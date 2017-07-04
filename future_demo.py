# /usr/bin/env python
# coding=utf8
# create by caokun on 2017-06-30

"""
__future__模块测试。
__slots__  限制类的属性，不生成 __dict__,只能给对象设置出现的值。
property  把方法变成属性的装饰器，有些敏感数据，不应该暴露在外面。
"""

from __future__ import unicode_literals, division


print "'xxx' is unicode? {}".format(isinstance('xxx', unicode))
print "'xxx' is unicode? {}".format(isinstance(u'xxx', unicode))
print "'xxx' is str? {}".format(isinstance('xxx', str))
print "'xxx' is str? {}".format(isinstance(b'xxx', str))


print '10 / 3 = {}'.format(10 / 3)
print '10 // 3 = {}'.format(10 // 3)  # 地板除