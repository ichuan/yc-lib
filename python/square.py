#!/usr/bin/python
# solution for http://www.blueidea.com/tech/program/2010/7784.asp
try:
    n = int(raw_input('Input a number: '))
except ValueError:
    print 'Not a valid number\n'
    exit(1)
n = n + 1
half = n / 2
for i in range(1, n + 1):
    for j in range(1, n + 1):
        if (i + j) / 2 <= half:
            print i if i < j else j,
        else:
            i1 = n - j + 1
            j1 = n - i + 1
            print i1 if i1 < j1 else j1,
    print
