#!/usr/bin/env python
# coding: utf-8
# yc@2013/07/31

'''
生成缩略图
比例不一致时以宽度为准；裁切掉超过比例的部分
'''

import sys
from PIL import Image


# 缩略图大小
SIZE = (200, 300)

def thumb(in_file, out_file):
	'''
	'''
	im = Image.open(in_file)
	ratio = im.size[0] * 1.0 / SIZE[0]
	# 原图宽度大于缩略图时才做缩放
	if ratio > 1:
		new_height = int(im.size[1] / ratio)
		im = im.resize((SIZE[0], new_height), Image.ANTIALIAS)
	# 高度过长时进行裁切
	if im.size[1] > SIZE[1]:
		im = im.crop((0, 0, im.size[0], SIZE[1]))
	im.save(out_file)


if __name__ == '__main__':
	if len(sys.argv) == 3:
		thumb(sys.argv[1], sys.argv[2])
	else:
		print 'Usage: python %s <image_in> <image_out>' % sys.argv[0]
