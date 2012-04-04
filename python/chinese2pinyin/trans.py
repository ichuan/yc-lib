#!/usr/bin/env python
# coding: utf-8
# yc@2012/4/4
# db from http://xh.5156edu.com/zmj.php.js

'''
usage : python trans.py 我 的 世 界
output: wǒ de shì jiè
'''

import cPickle

py = None

def _trans(i):
	global py
	if py is None:
		py = cPickle.load(open('./py.db'))
	return py[i] if i in py else i

if __name__ == '__main__':
	for i in sys.argv[1:]:
		print _trans(i.strip().decode('utf-8')), 
