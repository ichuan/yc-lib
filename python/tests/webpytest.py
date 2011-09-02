#!/usr/bin/env python
# coding:utf-8

import web

url = (
	r'/(.*)', 'index',
)
render = web.template.render('tpls/')

app = web.application(url, globals())

class index(object):
	'''
	'''
	def GET(self, name):
		return render.index(name)

if __name__ == '__main__':
	app.run()
