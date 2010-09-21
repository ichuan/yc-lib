#!/usr/bin/python

a,b=(1,2)
s=b
while b < 4000000:
    a,b=(b,a+b)
    if b % 2 == 0: s += b
print s
