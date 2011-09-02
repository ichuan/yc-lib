#!/usr/bin/env python
# coding: utf-8
# yc@2011-05-31 11:14:25

import httplib
from urlparse import urlsplit

urls = [
	u'http://192.168.10.205/webapp/test1/web_scanner_test_file.txt',
	u'http://192.168.10.205/webapp/test1/admin/',
	u'http://192.168.10.205/auth/pre_login/register.php',
	u'http://192.168.10.205/webapp/test1/left.asp',
	u'http://192.168.10.205/perfomance/delay_20s.php',
	u'http://192.168.10.205/auth/pre_login/index.php',
	u'http://192.168.10.205/auth/pre_login/login.php',
	u'http://192.168.10.205/webapp/test1/data/',
	u'http://192.168.10.205/webapp/test1/foot.asp',
	u'http://192.168.10.205/auth/pre_login/forgot_password.php',
	u'http://192.168.10.205/perfomance/delay_10s.php',
	u'http://192.168.10.205/webapp/test1/about.asp',
	u'http://192.168.10.205/webapp/test1/dg.asp',
	u'http://192.168.10.205/webapp/test1/NewsMore.asp',
	u'http://192.168.10.205/webapp/test1/mal.asp',
	u'http://192.168.10.205/webapp/test1/shopmore.asp',
	u'http://192.168.10.205/webapp/test1/search_news.asp',
	u'http://192.168.10.205/webapp/test1/job.asp',
	u'http://192.168.10.205/webapp/test1/News.asp'
]

#urls = ['http://67.23.177.211/100mb.bin']

for i in urls:
	if i.startswith('https'):
		cls = httplib.HTTPSConnection
	else:
		cls = httplib.HTTPConnection
	parts = urlsplit(i)
	conn = cls(parts.netloc,timeout=10)
	try:
		conn.request('GET', parts.path, headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.65',
		})
		res = conn.getresponse()
		print res.status, i
		conn.close()
	except:
		print 'pass ', i
