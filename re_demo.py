#!/usr/bin/env python
# coding=utf8

"""
create on 2017-11-22
"""

__author__ = 'cao kun'


import re


p_email = r'\w+@(?P<label>\w+)\.(?P<ext>\w+)'
print re.match(p_email, '1312567898@qq.com').group()


p_phone = r'((13[0-9])|(14[5, 6, 7])|(15[0-3, 5-9])|(177)|(18[0, 5-9]))\d{8}$'
print re.match(p_phone, '15922224175').group()
