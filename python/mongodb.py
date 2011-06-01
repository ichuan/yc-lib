#!/usr/bin/env python

import datetime
from pymongo import Connection

conn = Connection('localhost', 27017)
db = conn.dbapi

test = db.table1
test.insert({
	'id': 1,
	'name': 'test1', 
	'desc': ['just', 'a', 'test'],
	'date': datetime.datetime.now(),
})

print test.count()
print test.find_one()
test.drop()
