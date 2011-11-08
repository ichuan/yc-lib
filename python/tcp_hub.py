#!/usr/bin/env python
# coding: utf-8
# yc@2011/11/08
# usage: python tcp_hub.py -a 0.0.0.0:1021 -b 1234 -v

from __future__ import with_statement
import socket, re, sys, threading
from optparse import OptionParser

def parse_cmd():
	re_ip_port = r'^(?P<addr>.+:)?(?P<port>[0-9]{1,5})$'

	parser = OptionParser(usage='%prog -a [host:]port -b [host:]port [-v]', version='%prog 1.0')
	parser.add_option('-a', dest='a', help='local addr1(optional) & port1: 0.0.0.0:123 or 123')
	parser.add_option('-b', dest='b', help='local addr2(optional) & port2: 0.0.0.0:456 or 456')
	parser.add_option('-v', dest='verbose', default=False, action='store_true', help='print stat to screen')

	options, args = parser.parse_args()
	if not options.a or not options.b:
		parser.print_usage()
		sys.exit(-1)

	x = re.match(re_ip_port, options.a)
	if not x:
		parser.error('addr a format error!')
	addr1 = x.group('addr') or '0.0.0.0'
	addr1 = addr1.rstrip(':')
	port1 = x.group('port')
	if not port1:
		parser.error('specify port1 plz!')
	port1 = int(port1)

	x = re.match(re_ip_port, options.b)
	if not x:
		parser.error('addr b format error!')
	addr2 = x.group('addr') or '0.0.0.0'
	addr2 = addr2.rstrip(':')
	port2 = x.group('port')
	if not port2:
		parser.error('specify port2 plz!')
	port2 = int(port2)

	verbose = options.verbose

	return addr1, port1, addr2, port2, verbose

log_lock = threading.Lock()
def log(msg):
	if verbose:
		with log_lock:
			print msg

def sock_proxy(sock_in, sock_out):
	addr_in = '%s:%d' % sock_in.getpeername()
	addr_out = '%s:%d' % sock_out.getpeername()

	while True:
		try:
			data = sock_in.recv(4096)
		except Exception, e:
			log('Socket read error of %s: %s' % (addr_in, str(e)))
			break

		if not data:
			log('Socket closed by ' + addr_in)
			break

		try:
			sock_out.sendall(data)
		except Exception, e:
			log('Socket write error of %s: %s' % (addr_out, str(e)))
			break

		log('%s => %s (%d bytes)' % (addr_in, addr_out, len(data)))

	sock_in.close()
	sock_out.close()

def new_clients(addr, port, a2, p2):
	sock_main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_main.bind((addr, port))
	sock_main.listen(1)
	log('Listening at %s:%d ...' % (addr, port))

	sock, addr2 = sock_main.accept()
	log('New clients from %s:%d ...' % addr2)
	sid = '%s:%d' % (addr, port)
	sid2 = '%s:%d' % (a2, p2)
	G[sid]['sock'] = sock
	G[sid]['signal'].set()
	G[sid2]['signal'].wait()

	sock_proxy(sock, G[sid2]['sock'])
	sock_main.close()

addr1, port1, addr2, port2, verbose = parse_cmd()
G = {
	'%s:%d' % (addr1, port1): {
		'sock': None,
		'signal': threading.Event(),
	},
	'%s:%d' % (addr2, port2): {
		'sock': None,
		'signal': threading.Event(),
	},
}
t1 = threading.Thread(target=new_clients, args=(addr1, port1, addr2, port2))
t2 = threading.Thread(target=new_clients, args=(addr2, port2, addr1, port1))

try:
	t1.start()
	t2.start()
	t1.join()
	t2.join()
except (KeyboardInterrupt, SystemExit):
	log('Closing...')
