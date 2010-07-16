#!/usr/bin/env python
def func():
    print 'first time called'
    a = 1234
    global func
    func = lambda : a
    return a

print func()
print func()
print func()
print func()
print func()
