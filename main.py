# -*- coding: utf-8 -*-
import web
from handle import Handle
urls = ('/wx', 'Handle',)
# class Handle(object):
#    def GET(self):
#        return "KK V587"
if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

