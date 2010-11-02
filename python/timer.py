#!/usr/bin/env python
# coding: utf-8

from threading import Timer
from datetime import datetime

class Hello:
    def __init__(self):
        self.t = Timer(2.0, self.work)
        self.t.start()

    def work(self):
        print datetime.now().isoformat(' ')

if __name__ == '__main__':
    a = Hello()
