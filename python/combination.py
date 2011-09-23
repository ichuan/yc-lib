#!/usr/bin/env python
# coding: utf-8
# yc@2011/09/05

import copy

def combination(arr, m, callback):
	'''
	从 arr 数组中取 m 个元素组成一个新数组，调用 callback 处理
	也就是数学中的“组合” http://911.im/5
	全排列可以用itertools里的product：http://911.im/i
	'''
	n = len(arr)

	if m == 1:
		return [callback([i]) for i in arr]

	if n <= m:
		return callback(copy.copy(arr))

	for i in range(n - m + 1):
		combination(arr[i + 1:], m - 1, lambda x:callback(x.insert(0, arr[i]) or x))

if __name__ == '__main__':
	def cb(x): print x

	combination(range(10), 2, cb)
