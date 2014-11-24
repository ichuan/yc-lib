#!/usr/bin/env python
# coding: utf-8
# yc@2014/10/13

import random


def randfloat(a, b, precision=None):
  '''
  Return random float in range [a, b], including both end points.
  If precision is None, it is the longer precision of a and b
  '''
  if precision is None:
    precision = 0
    a1, b1 = str(a).lstrip('0123456789'), str(b).lstrip('0123456789')
    if a1.startswith('.'):
      precision = len(a1) - 1
    if b1.startswith('.'):
      precision = max(precision, len(b1) - 1)
  mul = pow(10, precision)
  return random.randint(int(a * mul), int(b * mul)) * 1.0 / mul


if __name__ == '__main__':
  # 1 or 2
  print randfloat(1, 2)
  # 1.0000 to 2.0000
  print randfloat(1, 2, precision=4)
  # 1.234000 to 2.3456789
  print randfloat(1.234, 2.3456789)
