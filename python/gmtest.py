#!/usr/bin/env python
# coding:utf-8

import threading, time
from pymongo import Connection


lock = threading.RLock()
cond = threading.Condition()
table = Connection().test.tablex
table.drop()
table.insert({'x': 0})

def target():
	cond.acquire()
	cond.wait()
	lock.acquire()
	i = table.find_one({'x': 0})
	if i:
		# found it
		table.update({'_id': i['_id']}, {'$set': {'x': 1}})
	lock.release()
	cond.release()
	if i:
		print '\n%s got i' % threading.current_thread()

for i in range(20):
	t = threading.Thread(target=target)
	t.start()

time.sleep(1)
cond.acquire()
cond.notifyAll()
cond.release()
