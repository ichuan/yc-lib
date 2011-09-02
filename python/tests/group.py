#!/usr/bin/env python
# coding: utf-8
# yc@2011-05-30 13:33:34

import pymongo
from pprint import pprint

db = pymongo.Connection('mongodb://127.0.0.1')['test']

base = db.base

r = '''
function (doc, out){
	out.count += 1;
}
'''
pprint(base.group(['content_type'], {}, {'count': 0}, r))
