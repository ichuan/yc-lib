#!/usr/bin/env python
# coding: utf-8
# yc@2010-11-01
'''
a simple multi-thread crawler
'''

from Queue import Queue, Empty
from datetime import datetime
from optparse import OptionParser
from urllib import urlopen
from urlparse import urlparse
import time, random, threading, bsddb, sys, os, re

#url_pattern  = re.compile(r'^(https?)://([a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)+)(/?.*)$')
url_pattern  = re.compile(ur'^https?://[^.]+(\.[^.]+)+.*$', re.IGNORECASE)
link_pattern = re.compile(ur'<a\s+href="([^"]+)', re.IGNORECASE)
trim_hash    = re.compile(ur'#.*')
trim_script  = re.compile(ur'<script[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE)
meta_charset = re.compile(ur'''<meta[^>]+charset=["']?([a-zA-Z0-9\-]+)''')
header_charset = re.compile(ur'charset=(.+)$')

class yccrawler:
    '''
    a simple multi-thread crawler filtering webpages by keyword.
    pages containing the specified keyword will be stored in a bdb file. with no keyword supplied, all pages crawled will be stroed.
    crawling status will be print on screen every one(default) second.
    '''
    def __init__(self, options):
        self.url_queue     = Queue() # thread-safe Queue
        self.options       = options
        self.count_crawled = 0
        self.count_hit     = 0
        self.current_url   = options.starturl
        self.lock          = threading.RLock()
        self.all_done      = False
        self.status_inteval= 1
        if options.starturl:
            self.url_queue.put((trim_hash.sub('', options.starturl), 1)) # item in queue is tuple: (url, depth)

    def list_urls(self):
        '''
        list urls in previous saved bdb file
        '''
        self.__open_bdb()

        count = 0
        for url, html in self.dbh.iteritems():
            count += 1
            print '%s (%d bytes)' % (url, len(html))
        print '%d urls total' % count

        self.__close_bdb()

    def __open_bdb(self):
        '''
        open bdb file with hashopen(), exit when exception occurs(eg: pemition denied)
        '''
        try:
            self.dbh = bsddb.hashopen(options.dbfile)
        except Exception, e:
            print e
            sys.exit(-1)

    def __close_bdb(self):
        self.dbh.close()

    def dispatch(self):
        '''
        the main loop. start several crawling thread and one status thread, wait till all urls are crawled(according to options.depth)
        '''
        self.__open_bdb()

        # start the crawl thread
        for i in range(self.options.threads):
            threading.Thread(target=self.crawl_thread).start()

        # start the status thread
        threading.Thread(target=self.status_thread).start()

        self.url_queue.join()
        self.all_done = True
        self.__close_bdb()

        time.sleep(self.status_inteval)
        print 'all done, %d urls crawled, %d urls containing %s' % (self.count_crawled, self.count_hit, self.options.keyword)

    def crawl_thread(self):
        '''
        crawler thread. use thread-safe Queue to retrieve and save newly founded urls.
        use the simple str.find() to determine if keyword is in that page
        '''
        while not self.all_done:
            try:
                url, depth = self.url_queue.get_nowait()
            except Empty:
                time.sleep(1)
                continue

            if self.dbh.has_key(url):
                self.url_queue.task_done()
                continue

            #print '[%s] trying %s...' % (threading.current_thread().getName(), url)
            try:
                fd   = urlopen(url)
                html = fd.read()
                info = fd.info()
                fd.close()
            except IOError, e:
                self.url_queue.task_done()
                continue

            # ignore non-text urls
            if info.getmaintype() != 'text':
                self.url_queue.task_done()
                continue

            # convert charset to `utf-8` if needed
            charset = self.get_charset(info.getheader('Content-Type'), html)
            if charset == 'gb2312':
                charset = 'gbk' # bigger charset
            try:
                html = html.decode(charset)
            except LookupError:
                pass

            # save new urls to queue
            if depth < self.options.depth:
                depth += 1
                for link in link_pattern.findall(self.clean_html(html)):
                    link = self.valid_link(link, url)
                    if link:
                        self.url_queue.put_nowait((link.encode('utf-8'), depth)) # bdb does not support unicode key

            self.lock.acquire()
            if self.options.keyword is None or html.find(self.options.keyword) != -1:
                # save to bdb
                self.dbh[url] = html.encode('utf-8')
                self.count_hit += 1
                
            self.count_crawled += 1
            self.current_url = url
            self.lock.release()

            self.url_queue.task_done()

    def get_charset(self, header, html, default='gbk'):
        '''
        get webpage charset from http header or html, return default charset if failed
        '''
        if header is not None:
            obj = header_charset.search(header.lower())
            if obj:
                return obj.group(1)

        obj = meta_charset.search(html)
        if obj:
            return obj.group(1)

        try:
            html.decode(default)
        except:
            default = 'utf-8'
        return default

    def clean_html(self, html):
        '''
        clean a html, eg: remove scripts, styles, and other useless tags
        '''
        return trim_script.sub('', html)

    def valid_link(self, url, current_url):
        '''
        determine if a url is of the same domain with us, organize relative url to absolute url if needed
        '''
        url = trim_hash.sub('', url.strip())

        if url == '' or url.startswith('javascript'):
            return None

        parsed_url = urlparse(current_url)

        # process absolute links like 'http://xxx/xxx'
        if url_pattern.match(url):
            return url if self.is_our_url(url, parsed_current_url = parsed_url) else None

        # process relative links like '/a/b/c.html' or 'a/b/c.html'
        path = '/' if parsed_url.path == '' else os.path.dirname(parsed_url.path) + '/'
        if url.startswith('/'):
            return '%s://%s%s' % (parsed_url.scheme, parsed_url.netloc, url)
        return '%s://%s%s%s' % (parsed_url.scheme, parsed_url.netloc, path, url)

    def is_our_url(self, url, current_url = None, parsed_current_url = None):
        '''
        judge if a url is under a domain, used by valid_link()
        eg:
            is_our_url('http://news.163.com/a', 'www.163.com') => True
            is_our_url('http://news.163.com', '163.com') => True
            is_our_url('http://tech.163.com', 'www.sohu.com') => False
            is_our_url('http://tech.163.com', 'news.163.com') => False
        '''
        if parsed_current_url is None:
            parsed_current_url = urlparse(current_url)
        root_domain = parsed_current_url.netloc[3:] if parsed_current_url.netloc.split('.')[0] == 'www' else '.' + parsed_current_url.netloc
        domain = urlparse(url).netloc
        return domain.find(root_domain) == len(domain) - len(root_domain)

    def status_thread(self):
        '''
        status thread, print crawling status every self.status_inteval seconds, exit when all urls are crawled
        '''
        while not self.all_done:
            time.sleep(self.status_inteval)
            total = self.url_queue.qsize() + self.count_crawled
            percent = (self.count_crawled / float(total) * 100) if total != 0 else 100.0 
            print 'Progress: %.2f%%, %d/%d/%d(hit/crawled/total), current url: %s' % (percent, self.count_hit, self.count_crawled, total, self.current_url)

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option('-s', '--starturl', dest='starturl', help='the initial url where crawler start')
    parser.add_option('-d', '--depth', dest='depth', help='the depth of urls to crawl according to the initial url. (default: 3)', default=3, type='int')
    parser.add_option('-t', '--threads', dest='threads', help='how many threads should be used. (default: 5)', default=5, type='int')
    parser.add_option('-f', '--dbfile', dest='dbfile', help='the file where data should be saved')
    parser.add_option('-k', '--key', dest='keyword', help='the keyword to search')
    parser.add_option('-l', '--list', dest='list', help='list the urls in a bsddb file specified by -f', action='store_true')

    options, args = parser.parse_args()
    c = yccrawler(options)

    if options.list:
        if options.dbfile and os.path.isfile(options.dbfile):
            c.list_urls()
            sys.exit(0)
        else:
            parser.error('use -f to specify a bsddb file')
    if options.starturl is None or url_pattern.match(options.starturl) is None:
        parser.error('use -s option to specify a correct url')
    if options.depth <= 0:
        parser.error('depth option must be bigger than zero')
    if options.threads <= 0:
        parser.error('threads option must be bigger than zero')
    if options.dbfile is None or os.path.isfile(options.dbfile):
        parser.error('use -f option to specify a new file for data storing')

    options.keyword = options.keyword.decode('utf-8') # convert utf-8 to unicode
    c.dispatch()
