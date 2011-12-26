#!/usr/bin/env python
# coding: utf-8
# yc@2011/12/23

# 统计 csdn 密码库中 "安全密码" 的个数

def strong_passwd(passwds):
	'''
	安全密码：(http://911.im/S)
		1. 6 ~ 16 个字符
		2. 英文字母 + 数字 + 特殊字符
	'''
	for i in passwds:
		if 6 <= len(i) <= 16:
			flag = 0
			for j in i:
				if '0' <= j <= '9':
					flag |= 4
				elif 'A' <= j <= 'Z' or 'a' <= j <= 'z':
					flag |= 2
				elif j in '!@#$%^&*':
					flag |= 1
				if flag == 7:
					yield i
					break

logs = open('www.csdn.net.sql')
passwds = (i[i.find('#')+1 : i.rfind('#')].strip() for i in logs)
print sum(1 for i in strong_passwd(passwds))
