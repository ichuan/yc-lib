#!/usr/bin/env python
# coding: utf-8
# yc@2016/07/02

import os
import json
import time
import random
import urllib2
import httplib
from urlparse import urlparse
from socket import error as SocketError
from decimal import Decimal


HTTP_TIMEOUT = 10
TEMP_DIR = '/tmp/bitbar-ticker/'
TICKERS = {
    'lsk': {
        'url': 'https://api.coinmarketcap.com/v1/ticker/lisk/?convert=CNY',
        'pop': lambda i: json.loads(i)[0]['price_cny'],
        'sym': u'¥',
    },
    'btc': {
        'url': 'https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=CNY',
        'pop': lambda i: json.loads(i)[0]['price_cny'],
        'sym': u'¥',
    },
    'ltc': {
        'url': 'https://api.coinmarketcap.com/v1/ticker/litecoin/?convert=CNY',
        'pop': lambda i: json.loads(i)[0]['price_cny'],
        'sym': u'¥',
    },
}


def http_get(url, try_times=1):
    req = urllib2.Request(url, headers={'Cache-Control': 'max-age=0'})
    for i in range(try_times, 0, -1):
        try:
            return urllib2.urlopen(req, timeout=HTTP_TIMEOUT).read()
        except (urllib2.HTTPError, urllib2.URLError,
                httplib.BadStatusLine, SocketError):
            if i == 1:
                raise
            time.sleep(random.random())


def normalize(val, precision=4):
    fmt = '%%.%df' % precision
    return Decimal(fmt % float(val)).normalize()


def fetch(item, data_file=None):
    conf = TICKERS[item]
    prev = 0
    if data_file and os.path.isfile(data_file):
        try:
            prev = float(open(data_file).read())
        except:
            pass
    try:
        val = float(conf['pop'](http_get(conf['url'])))
        if val == prev:
            color = 'black'
        elif val > prev:
            color = 'red'
        else:
            color = 'green'
        if data_file:
            open(data_file, 'w+').write(str(val))
        sym = conf['sym']
        val = normalize(val)
    except:
        val = 'ERR'
        color = 'red'
        sym = ''
    name = conf.get('name', item.upper())
    out = u'%s: %s%s | color=%s' % (name, sym, val, color)
    print out.encode('utf-8')
    print '---'
    domain = urlparse(conf['url']).netloc
    print '%s | href=http://%s' % (domain, domain)


def main():
    if not os.path.isdir(TEMP_DIR):
        try:
            os.makedirs(TEMP_DIR)
        except:
            pass
    filename = os.path.basename(__file__)
    data_file = '%s%s.dat' % (TEMP_DIR, filename)
    try:
        item = filename.split('.')[0]
        assert item in TICKERS
    except:
        item = 'lsk'
    fetch(item, data_file)


if __name__ == '__main__':
    main()
