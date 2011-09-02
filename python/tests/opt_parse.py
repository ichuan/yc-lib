#!/usr/bin/env python
# coding: utf-8

from optparse import OptionParser
from pprint import pprint
import re, os

parser = OptionParser()
url_pattern = re.compile(r'^https?://.+')

parser.add_option('-s', '--starturl', dest='starturl', help='the initial url where crawler start')
parser.add_option('-d', '--depth', dest='depth', help='the depth of urls to crawl according to the initial url', default=3, type='int')
parser.add_option('-t', '--threads', dest='threads', help='how many threads should be used', default=5, type='int')
parser.add_option('-f', '--dbfile', dest='dbfile', help='the file where data should be saved')
parser.add_option('-k', '--key', dest='keyword', help='the keyword to search')

options, args = parser.parse_args()
#pprint(options)

if options.starturl is None or url_pattern.match(options.starturl) is None:
    parser.error('use -s option to specify a correct url')
if options.depth <= 0:
    parser.error('depth option must be bigger than zero')
if options.threads <= 0:
    parser.error('threads option must be bigger than zero')
if options.dbfile is None or os.path.isfile(options.dbfile):
    parser.error('use -f option to specify a new file for data storing')
