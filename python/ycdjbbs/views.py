#!/usr/bin/env python
# encoding=utf-8
# yc

from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime

def current_datetime(request, offset = 0):
    offset = int(offset)
    now = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render_to_response('time.html', locals())
