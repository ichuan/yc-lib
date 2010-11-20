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
from urllib import urlencode

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api.urlfetch import fetch

'''
auto checkin for xiami.com
'''

TASKS = ['xiami_checkin']
# log in to your xiami.com account, paste `javascript:alert($.cookie('auth'))` in the address
# bar and hit enter, you'll get the following AUTH code
AUTH ='60bRnVHLWWfAdKThkK/IoBGddQ10CHZAiEK11xUJSl4jRroPwE5F7m+Sr+PayYihLYk'

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class TaskHandler(webapp.RequestHandler):
    def get(self, task_id):
        '''
        task handler. Mostly, this is called by the cron task
        '''
        try:
            ret = {
                'xiami_checkin': self._xiami_checkin,
            }[task_id]()
        except:
            self.response.set_status(404)
            self.response.out.write('404 Not Found')
            return

        if not ret:
            self.response.out.write('Unable to complete task')
        else:
            self.response.out.write('Task done')

    def _xiami_checkin(self):
        '''
        checkin task for xiami.com
        '''
        headers = {
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-cn,zh;q=0.5',
            'Accept-Encoding': 'deflate',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            'Content-Type': 'application/xml',
            'Referer': 'http://www.xiami.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12',
            'Cookie': urlencode({'auth': AUTH}),
        }
        try:
            obj = fetch('http://www.xiami.com/task/signin', method='POST', headers=headers)
            ret = obj.content.strip()
        except Exception, e:
            ret = ''
        finally:
            return bool(ret)


def main():
    application = webapp.WSGIApplication([
        (r'/', MainHandler),
        (r'/task/(.+)', TaskHandler),
        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
