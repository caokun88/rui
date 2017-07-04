# /usr/bin/env python
# coding=utf8
# create by caokun on 2017-06-30

from wsgiref.simple_server import make_server

from client import application


httpd = make_server('', 9999, application)
print 'Serving HTTP on 9999...'
httpd.serve_forever()
