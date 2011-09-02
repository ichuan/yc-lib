#!/usr/bin/env python
# coding: utf-8

from Queue import Queue, Empty
from datetime import datetime
import time, random, threading

q = Queue()
l = threading.RLock()
q.put(1)

def time_thread():
    while True:
        d = None
        l.acquire()
        try:
            d = q.get_nowait()
        except Empty:
            print 'empty queue'
            l.release()
            break
        if d is not None:
            print 'in %s: %d (qsize: %d)' % (threading.current_thread().getName(), d, q.qsize())
            if d < 20:
                q.put(d + 2)
            q.task_done()
        l.release()
        time.sleep(random.random())

for i in range(4):
    t = threading.Thread(target=time_thread)
    print 'starting thread %d...' % (i + 1)
    t.start()

q.join()
print 'all done'
