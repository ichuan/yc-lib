#!/usr/bin/env python
# coding: utf-8
# yc@2016/07/02

import os
import json
import time
import random
import urllib2
import httplib
from urlparse import urlparse
from socket import error as SocketError


HTTP_TIMEOUT = 10
TEMP_DIR = '/tmp/bitbar-ticker/'
TICKERS = {
    'lsk': {
        'url': 'https://bitbays.com/api/v1/ticker/?market=lsk_cny',
        'pop': lambda i: json.loads(i)['result']['last'],
        'sym': u'¥',
    },
    'btc': {
        'url': 'https://www.okcoin.cn/api/v1/ticker.do?symbol=btc_cny',
        'pop': lambda i: json.loads(i)['ticker']['last'],
        'sym': u'¥',
    },
}


def http_get(url, try_times=1):
    req = urllib2.Request(url, headers={'Cache-Control': 'max-age=0'})
    for i in range(try_times, 0, -1):
        try:
            return urllib2.urlopen(req, timeout=HTTP_TIMEOUT).read()
        except (urllib2.HTTPError, urllib2.URLError,
                httplib.BadStatusLine, SocketError):
            if i == 1:
                raise
            time.sleep(random.random())


def fetch(item, data_file=None):
    conf = TICKERS[item]
    prev = 0
    if data_file and os.path.isfile(data_file):
        try:
            prev = open(data_file).read()
        except:
            pass
    try:
        val = conf['pop'](http_get(conf['url']))
        if val == prev:
            color = 'black'
        elif float(val) > float(prev):
            color = 'red'
        else:
            color = 'green'
        if data_file:
            open(data_file, 'w+').write(val)
        sym = conf['sym']
    except:
        val = 'ERR'
        color = 'red'
        sym = ''
    name = conf.get('name', item.upper())
    out = u'%s: %s%s | color=%s' % (name, sym, val, color)
    print out.encode('utf-8')
    print '---'
    domain = urlparse(conf['url']).netloc
    print 'From: %s | href=http://%s' % (domain, domain)


def main():
    if not os.path.isdir(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    filename = os.path.basename(__file__)
    data_file = '%s%s.dat' % (TEMP_DIR, filename)
    try:
        item = filename.split('.')[0]
        assert item in TICKERS
    except:
        item = 'lsk'
    fetch(item, data_file)


if __name__ == '__main__':
    main()
