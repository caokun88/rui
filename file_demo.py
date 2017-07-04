# /usr/bin/env python
# coding=utf8
# create by caokun on 2017-06-30


import codecs


f = codecs.open('file_test.txt', 'wb', encoding='utf8')
f.write('\n')
f.write(u'我是曹昆')
f.write('\n')
f.write(u'你是谁！')