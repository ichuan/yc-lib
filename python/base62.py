#!/usr/bin/env python
# coding: utf-8
# yc@2011/09/02

'''
62进制工具
'''
import re

__all__ = ['decto62', 'decfrom62']
chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def decto62(dec):
	'''
	十进制转62进制，输入数字，返回字串
	from: http://goo.gl/YDiCm
	'''
	ret = []
	while True:
		dec, a = divmod(dec, 62)
		ret.append(chars[a])
		if dec == 0:
			break
	ret.reverse()
	return ''.join(ret)

def decfrom62(num):
	'''62进制转十进制'''
	assert re.match(r'^[0-9a-zA-Z]+$', num)
	num = list(num)
	num.reverse()
	return reduce(lambda x,y:x+chars.find(num[y])*(62**y), range(len(num)), 0)
	

if __name__ == '__main__':
	assert decto62(192848) == 'Oas'
	assert decfrom62('Oas') == 192848
	print decto62(19999999999999999999999)
	print decfrom62('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
