#!/usr/bin/env python
# coding: utf-8
# yc@2012/03/01

def paginator(total_pages, current_page, window_size):
	'''
	html paginator helper
	'''
	start = current_page - window_size / 2
	if start < 1:
		start = 1
	end = start + window_size - 1
	if end > total_pages:
		start = max(1, start - (end - total_pages))
		end = total_pages
	return range(start, end + 1)

# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print paginator(100, 2, 10)
# [14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
print paginator(100, 19, 10)
# [91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
print paginator(100, 98, 10)

