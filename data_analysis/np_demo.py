# /usr/bin/env python
# coding=utf8

import numpy as np


a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [3, 4, 5]])

print a, a.dtype, a.shape
print b, b.dtype, b.shape
print c, c.dtype, c.shape
c.shape = (2, -1)    # 当某个轴的元素为-1时，将根据数组元素的个数计算此轴的长度
print c, c.dtype, c.shape

# reshape  可以创建一个改变了尺寸的新数组，原数组的shape保持不变。

d = a.reshape(3, -1)  # 此时a数组保持不变
print d

# 现在 a和d 共享数据存储内存区域，因此，修改任意一个数组中的数据，另一个数组中对应的数据也会跟着一起修改。

d[0] = 100
print a
print d

# dtype 属性 可以查看数组的元素类型。也可以在创建数组的时候 定义数组元素的类型。

f = np.array([1, 3, 5, 7, 9], dtype=np.complex)
print f

# 上面例子通过python的list创建数组，效率不是很高，可以通过numpy的专门创建数组的函数来创建数组。

# arange 函数类似于python 的 range函数，通过指定开始、终止、步长，来创建一维数组。（不包括终止值）

arange_array = np.arange(1, 2, 0.1, dtype=np.float)
print arange_array

# linspace 创建等差一维数组，指定 开始值，终止值，元素个数，可以通过endpoint关键字指定是否包括终止值（默认包括终止值）

linspace_array = np.linspace(1, 3, 15, endpoint=False)
print linspace_array

# logspace 创建等比一维数组，指定 开始值，终止值，元素个数，可以通过endpoint关键字指定是否包括终止值（默认包括终止值）
# 下面的例子产生10(10^1) ~ 100(10^2)，有13个元素的等比数组，但是endpoint=False 就是不包含终止值。

logspace_array = np.logspace(1, 2, 13, endpoint=False)
print logspace_array

# 另外，还可以使用frombuffer， fromstring，fromfile等函数可以从字节序列创建数组，下面以fromstring为例：
# python的字符串其实是字节序列，每个字符占一个字节，因此如果从字符串s创建一个8bit的数组的话，所得到的数组正是这s字符串
# 中每个字符对应的ascii编码。
s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ~$%'
fromstring_array = np.fromstring(s, dtype=np.int8)
print fromstring_array

# fromfunction函数的第一个参数为计算每个数组元素的函数，第二个参数为数组的大小(shape)，
# 因为它支持多维数组，所以第二个参数必须是一个序列
func_array = np.fromfunction(lambda x, y: x % 4 + 1 + y, (10, 10))
print func_array


"""
Examples
    --------
    >>> np.arange(3)
    array([0, 1, 2])
    >>> np.arange(3.0)
    array([ 0.,  1.,  2.])
    >>> np.arange(3,7)
    array([3, 4, 5, 6])
    >>> np.arange(3,7,2)
    array([3, 5])
    
    >>> a = np.arange(10)
    >>> a[5]    # 用整数作为下标可以获取数组中的某个元素
    5
    >>> a[3:5]  # 用范围作为下标获取数组的一个切片，包括a[3]不包括a[5]
    array([3, 4])
    >>> a[:5]   # 省略开始下标，表示从a[0]开始
    array([0, 1, 2, 3, 4])
    >>> a[:-1]  # 下标可以使用负数，表示从数组后往前数
    array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    >>> a[2:4] = 100,101    # 下标还可以用来修改元素的值
    >>> a
    array([  0,   1, 100, 101,   4,   5,   6,   7,   8,   9])
    >>> a[1:-1:2]   # 范围中的第三个参数表示步长，2表示隔一个元素取一个元素
    array([  1, 101,   5,   7])
    >>> a[::-1] # 省略范围的开始下标和结束下标，步长为-1，整个数组头尾颠倒
    array([  9,   8,   7,   6,   5,   4, 101, 100,   1,   0])
    >>> a[5:1:-2] # 步长为负数时，开始下标必须大于结束下标
    array([  5, 101])
    
    
    当使用布尔数组b作为下标存取数组x中的元素时，将收集数组x中所有在数组b中对应下标为True的元素。
    使用布尔数组作为下标获得的数组不和原始数组共享数据空间，注意这种方式只对应于布尔数组，不能使用布尔列表。
    
    >>> x = np.arange(5,0,-1)
    >>> x
    array([5, 4, 3, 2, 1])
    >>> x[np.array([True, False, True, False, False])]
    >>> # 布尔数组中下标为0，2的元素为True，因此获取x中下标为0,2的元素
    array([5, 3])
    >>> x[[True, False, True, False, False]]
    >>> # 如果是布尔列表，则把True当作1, False当作0，按照整数序列方式获取x中的元素
    array([4, 5, 4, 5, 5])
    >>> x[np.array([True, False, True, True])]
    >>> # 布尔数组的长度不够时，不够的部分都当作False
    array([5, 3, 2])
    >>> x[np.array([True, False, True, True])] = -1, -2, -3
    >>> # 布尔数组下标也可以用来修改元素
    >>> x
    array([-1,  4, -2, -3,  1])
    
"""


# 布尔数组一般不是手工产生，而是使用布尔运算的ufunc函数产生，关于ufunc函数请参照 ufunc运算 一节。
