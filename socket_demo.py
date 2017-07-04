# /usr/bin/env python
# coding=utf8
# create by caokun on 2017-06-30

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.yuleke.com', 80))