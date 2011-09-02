#coding: utf-8

class a:
    def __call__(self, *x, **y):
        print 'called'
    def __init__(self):
        print 'inited'

b = a()
print 'instance b'
b()
