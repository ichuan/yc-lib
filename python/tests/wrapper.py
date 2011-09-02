#!/usr/bin/env python
def a(func):
    print "in wrapper now\n"
    return lambda *b,**c : func(*b, **c)

@a
def hello(name):
    print "hello, %s" % name
