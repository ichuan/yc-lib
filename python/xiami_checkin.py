#!/usr/bin/env python
# coding: utf-8

import urllib2, urllib
from cookielib import CookieJar

EMAIL = 'a@b.com'
PASSWD = 'pass'

# cookie support
urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar())))

# login
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'}
data = urllib.urlencode({'email': EMAIL, 'password': PASSWD, 'submit': '登 录'})
r = urllib2.Request('http://www.xiami.com/member/login', data=data, headers=headers)
urllib2.urlopen(r).read()

# checkin
headers['X-Requested-With'] = 'XMLHttpRequest'
headers['Referer'] = 'http://www.xiami.com/'
r = urllib2.Request('http://www.xiami.com/task/signin', data='', headers=headers)
print urllib2.urlopen(r).read()
