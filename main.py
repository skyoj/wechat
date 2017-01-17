# -*- coding: utf-8 -*-
import web
from handle import Handle
urls = ('/wx', 'Handle',)
class Handle(object):
#    def GET(self):
#        return "Hello this is a test"
if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

