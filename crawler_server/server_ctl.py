#!/usr/bin/env python

import json

from bs4 import BeautifulSoup
from tornado.web import Application, RequestHandler
from tornado.httpserver import HTTPServer
from tornado.options import define, options, parse_command_line
from tornado.ioloop import IOLoop

define("port", default=8888, type=int)

class ExampleHandler(RequestHandler):

    def get(self):

        who = self.get_argument('who', None)
        if who:
            self.write('hello' + who)
        else:
            self.write('hello world.')

    def post(self):

        #uid = self.get_argument('uid', None)
        #username = self.get_argument('username', None)
        #password = self.get_argument('password', None)

        #print uid
        #print username
        #print password

        self.write('your post a user.')

class UploadHtmlHandler(RequestHandler):

    def post(self):
        soup = BeautifulSoup(self.request.body)
        print 'title: ', str(soup.find_all('title'))[0]
        print 'body: ', soup.find_all('body')
        self.write('200')

class MyApplication(Application):

    def __init__(self):
        handlers = [
            (r'/', ExampleHandler),
            (r'/upload_html', UploadHtmlHandler),
        ]
        settings = dict()
        Application.__init__(self, handlers, settings)

def create_server():
    parse_command_line()
    http_server = HTTPServer(MyApplication())
    http_server.listen(options.port)
    IOLoop.instance().start()


