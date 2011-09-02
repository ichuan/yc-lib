#!/usr/bin/env python
def a():
    x=1
    try:
        print 'in try'
        return x
    finally:
        x=2
        print 'in finally'

print a()
