# /usr/bin/env python
# coding=utf8
# create by caokun on 2017-06-30

import json


def application_1(environ, start_response):
    print environ
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>hello world</h1>'


def application_name(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>name caokun</h1>'


def application_info(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>name caokun, sex 男, age 27</h1>'


def application_404(environ, start_response):
    start_response('404 OK', [('Content-Type', 'application/json')])
    return json.dumps({'code': 404, 'msg': '自定义404'})


URL_MAP = {
    '/': application_1,
    '/name': application_name,
    '/info': application_info
}


def application(environ, start_response):
    path = environ['PATH_INFO']
    print 'path == {}'.format(path)
    func = URL_MAP.get(path, application_404)
    print 'func == {}'.format(func.__name__)
    return func(environ, start_response)
