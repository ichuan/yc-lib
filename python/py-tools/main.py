#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import re

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api.urlfetch import fetch
from google.appengine.api import memcache

from config import *

'''
auto checkin for xiami.com
'''


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class TaskHandler(webapp.RequestHandler):
    '''
    '''

    headers = {
        'Accept': 'application/json, text/javascript, */*',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'deflate',
        'Accept-Charset': 'UTF-8,*;q=0.5',
        'Content-Type': 'application/xml',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
    }

    def get(self, task_id):
        '''
        task handler. Mostly, this is called by the cron task
        '''
        try:
            ret = {
                'xiami_checkin': self._xiami_checkin,
                'xiami_login': self._xiami_login,
            }[task_id]()
        except Exception, e:
            logging.error('Unable to complete task (%s)' % str(e))
            return
        logging.info('Task done(ret: %s)' % str(ret))

    def _xiami_login(self):
        '''
        login xiami.com and grab the authed cookies
        '''
        self.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cache-Control': 'no-cache',
        })
        auth = 'email=%s&password=%s&type=1&submit=1&autologin=1' % (EMAIL, PASSWORD)
        obj = fetch('http://www.xiami.com/member/login', method='POST', headers=self.headers, follow_redirects=False, payload=auth)
        ret = re.search(r'^(auth=[^;]+)', obj.headers['set-cookie']).group()
        memcache.set('cookie', ret)
        return ret

    def _xiami_checkin(self):
        '''
        checkin task for xiami.com
        '''
        cookie = memcache.get('cookie')
        if cookie is None:
            self._xiami_login()
            cookie = memcache.get('cookie')

        self.headers.update({
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://www.xiami.com/',
            'Cookie': cookie,
        })
        obj = fetch('http://www.xiami.com/task/signin', method='POST', headers=self.headers)
        return obj.content.strip()

def main():
    application = webapp.WSGIApplication([
        (r'/', MainHandler),
        (r'/task/(.+)', TaskHandler),
        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
