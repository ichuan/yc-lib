#!/usr/bin/env python
# coding:utf-8

import threading, logging
from urllib3 import connectionpool

connectionpool.log.setLevel(logging.DEBUG)
connectionpool.log.addHandler(logging.StreamHandler())
#pool = connectionpool.connection_from_url('http://5uproxy.net/http_fast.html', maxsize=10)
#
#def get():
#	for i in range(3):
#		pool.get_url('http://5uproxy.net/http_fast.html')
#
#for i in range(10):
#	threading.Thread(target=get).start()

pool = connectionpool.connection_from_url('www.python.org', maxsize=1)
pool.urlopen('GET', '/')
pool.urlopen('HEAD', '/')
pool.urlopen('HEAD', '/')
pool.urlopen('HEAD', '/')
pool.urlopen('HEAD', '/')
pool.urlopen('HEAD', '/')
