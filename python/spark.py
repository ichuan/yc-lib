#!/usr/bin/env python
# coding: utf-8
# yc@2011/11/16

import sys, math, re

ticks = '▁ ▂ ▃ ▄ ▅ ▆ ▇ █'.split()

if len(sys.argv) > 1:
	nums = ' '.join(sys.argv[1:])
else:
	nums = sys.stdin.read()

try:
	nums = map(float, re.split(r'[,;\s]', nums.strip(',;\t\n\r ')))
except:
	print 'Usage: python %s <numbers>' % sys.argv[0]
	sys.exit(1)

a, b = min(nums), max(nums)
sep = int(math.ceil((b - a) / len(ticks))) or sys.maxint

for i in nums:
	print ticks[int((i - a) / sep)], 
