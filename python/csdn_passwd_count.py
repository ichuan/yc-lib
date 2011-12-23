#!/usr/bin/env python
# coding: utf-8
# yc@2011/12/23

# 统计 csdn 密码库中 "安全密码" 的个数

from __future__ import with_statement
import re, string

def lines(path):
	'''
	每行形如：'siclj # lj7202 # junlu@peoplemail.com.cn'
	'''
	with open(path)	as f:
		for i in f:
			yield i

def passwd(lines):
	'''
	从一行字串中取出密码字串
	'''
	for i in lines:
		try:
			yield re.search(r'#\s*([^\s]+)', i).group(1)
		except:
			pass

def strong_passwd(passwds):
	'''
	安全密码：(http://911.im/S)
		1. 6 ~ 16 个字符
		2. 英文字母 + 数字 + 特殊字符
	'''
	for i in passwds:
		if (6 <= len(i) <= 16):
			flag = 0
			for j in i:
				if j in string.ascii_letters:
					flag |= 4
				elif j in string.digits:
					flag |= 2
				elif j in '!@#$%^&*':
					flag |= 1
				if flag == 7:
					yield i
					break

print sum(1 for i in strong_passwd(passwd(lines('www.csdn.net.sql'))))
