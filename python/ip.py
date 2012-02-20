#!/usr/bin/env python
# coding: utf-8
# yc@2012/02/20

def ip2long(ip):
	return reduce(lambda i, j:i + (j[0]<<j[1]), zip(map(int, ip.split('.')), [24, 16, 8, 0]), 0)

def long2ip(ip_int):
	return '.'.join(map(lambda i:str((ip_int>>i) & 0xFF), [24, 16, 8, 0]))

if __name__ == '__main__':
	a = '127.0.0.1'
	b = 2130706433

	assert ip2long(a) == b
	assert long2ip(b) == a

