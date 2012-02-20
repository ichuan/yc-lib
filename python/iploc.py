#!/usr/bin/env python
# coding: utf-8
# yc@2012/02/19
# 纯真ip库查询程序

import struct

__all__ = ['iploc']

MOD1 = '\x01'
MOD2 = '\x02'
DB_FILE = 'qqwry.dat'

def ip2long(ip):
	return reduce(lambda i, j:i + (j[0]<<j[1]), zip(map(int, ip.split('.')), [24, 16, 8, 0]), 0)

def long2ip(ip_int):
	return '.'.join(map(lambda i:str((ip_int>>i) & 0xFF), [24, 16, 8, 0]))

def bin_search(start, end, val, fp):
	'''
	二分查找ip所在范围，一般最大递归19次
	'''
	if start == end or start + 7 == end:
		# 找到了返回 ip 偏移
		# 没找到返回 ip 前一个偏移
		return start
	t = (end + 7 -start) / 7 / 2
	mid = start + t * 7
	fp.seek(mid)
	i = struct.unpack('I', fp.read(4))[0]
	if i == val:
		return mid
	elif i > val:
		return bin_search(start, mid, val, fp)
	else:
		return bin_search(mid, end, val, fp)

def read_str(fp):
	'''
	读取一个以\x00结尾的gbk字串
	'''
	r = []
	ch = fp.read(1)
	while ch != '\x00':
		r.append(ch)
		ch = fp.read(1)
	r = ''.join(r)
	return r.decode('gbk')

def offset_str(fp):
	'''
	fp当前下3字节为offset，读取位于offset处的字串
	'''
	offset = struct.unpack('I', fp.read(3) + '\x00')[0]
	fp.seek(offset)
	return read_str(fp)

def iploc(ip):
	'''
	纯真ip库结构见 http://lumaqq.linuxsir.org/article/qqwry_format_detail.html
	'''
	f = open(DB_FILE, 'rb')
	# ip索引起始地址
	i1 = struct.unpack('<i', f.read(4))[0]
	# ip索引结束地址
	i2 = struct.unpack('<i', f.read(4))[0]

	# 待查ip的整数形式
	ip_int = ip2long(ip)
	# 待查ip所在范围的地址
	ip_pos = bin_search(i1, i2, ip_int, f)
	f.seek(ip_pos)
	# 所在的起始ip范围
	range_start = long2ip(struct.unpack('I', f.read(4))[0])
	loc_pos = struct.unpack('I', f.read(3) + '\x00')[0]
	f.seek(loc_pos)
	# 所在的结束ip范围
	range_end = long2ip(struct.unpack('I', f.read(4))[0])
	# 所在地址，国家和地区
	loc1 = loc2 = ''
	# 索引模式
	mod = f.read(1)
	cur_pos = f.tell()
	if mod == MOD1:
		offset = struct.unpack('I', f.read(3) + '\x00')[0]
		f.seek(offset)
		# 二级模式
		mod = f.read(1)
		cur_pos = f.tell()
		if mod == MOD2:
			loc1 = offset_str(f)
			f.seek(cur_pos + 3)
			mod = f.read(1)
			if mod == MOD1 or mod == MOD2:
				loc2 = offset_str(f)
			else:
				f.seek(cur_pos + 3)
				loc2 = read_str(f)
		else:
			f.seek(cur_pos - 1)
			loc1 = read_str(f)
			loc2 = read_str(f)
	elif mod == MOD2:
		loc1 = offset_str(f)
		f.seek(cur_pos + 3)
		loc2 = read_str(f)
	# 无模式，直接读取位置
	else:
		f.seek(cur_pos - 1)
		loc1 = read_str(f)
		loc2 = read_str(f)
	f.close()

	return {
		'range_start': range_start,
		'range_end': range_end,
		'loc1': loc1,
		'loc2': loc2
	}

if __name__ == '__main__':
	import sys, re

	args = sys.argv
	if len(args) != 2:
		print 'Usage: python iploc.py <ip>'
		sys.exit(-1)

	ip = sys.argv[1].strip()
	if not re.match(
		r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
		ip
	):
		print 'Ip error: ' + ip
		sys.exit(-2)
	ret = iploc(ip)
	for i in ret:
		print (i + ':').ljust(14), ret[i]
