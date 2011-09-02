#!/usr/bin/env python
# coding: utf-8
# yc@2011-05-31 13:54:59

import threading, time

def t(a):
	time.sleep(1)
	print a.next()

y = iter(range(100))
ts = [threading.Thread(target=t, args=(y,)) for i in range(10)]
[x.start() for x in ts]
[x.join() for x in ts]
print 'done'
