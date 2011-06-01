#!/usr/bin/env python
# coding: utf-8
# yc@2011-05-30 13:33:34

import pymongo

db = pymongo.Connection('mongodb://127.0.0.1')['test']

base = db.base

scope = {
	'table' : {
		'application/postscript': 1,
		'application/javascript': 1,
		'application/x-javascript': 1,
		'application/x-sh': 1,
		'application/x-csh': 1,
		'application/xml': 1,
		'application/rss+xml': 1,
		'application/atom+xml': 1,
		'application/hta': 1,
		'application/sgml': 1,
		'application/xhtml+xml': 1,
		'application/vnd.google-earth.kml+xml': 1,
		'application/vnd.google-earth.kmz': 1,
		'application/vnd.mozilla.xul+xml': 1,
		'message/rfc822': 1,
	}
}
m = '''
function (){
	var ct = this.content_type;
	if (table[ct] !== undefined)
		key = table[ct];
	else if (ct.indexOf('text/') === 0)
		key = 1;
	else if (ct.indexOf('image/') === 0)
		key = 2;
	else
		key = 3;
	emit(key, {count: 1});
};
'''
r = '''
function (k, v){
	var res = {count: 0};
	v.forEach(function(i){
		res.count += i.count;
	});
	return res;
}
'''

out = base.map_reduce(m, r, 'mrtest', scope=scope)
#for i in out.find():
#	print i
#out.drop()
