# import time
# def timer(func):   #timer(test1)  func=test1
#     def deco(*args,**kwargs):
#         start_time = time.time()
#         func(*args,**kwargs)      #run test1
#         stop_time = time.time()
#         print("running time is %s"%(stop_time-start_time))
#     return deco
# @timer     # test1=timer(test1)
# def test1():
#     time.sleep(3)
#     print("in the test1")
# test1()

# def fib(max_num):
#     a,b = 1,1


#     while a < max_num:
#         yield b
#         a,b=b,a+b

# g = fib(20)               #生成一个生成器：[1，2, 3, 5, 8, 13]
# # print(g.__next__())
# # print(g.__next__())
# # print(g.__next__())         #第一次调用返回：1
# print(list(g))   


# l = list(range(1,101))
# def bin_search(data,val):

#    s = 0
#    e = len(data) - 1
#    while s <= e:
#       mid = (s+e)//2
#       if data[mid] == val:
#          return mid
#       elif data[mid] < val:
#          s = mid + 1
#       else:
#          e = mid - 1
#    return
# n = bin_search(l,11)
# print(n)        

# import request
# import redis
# #定义地址和端口
# host = '127.0.0.1'
# port = 6379


"""
remove  移除第一个匹配值
count 出现的次数
resverser 反转
index 第一个匹配对象下标
extend 合并列表
append 尾部追加 
insert 指定位置插入
pop  删除元素 默认最后一个
sort  排序

"""

"""
replace 以指定字符替换所有匹配的元素
split
join
strip
find


"""

"""
get
formkeys
cleaer（）
pop
setdefault 
update 更新字典
dict(zip(keys,values))
"""

"""
去重
& | -
"""

"""
进程是 资源分配的最小单位 ，程序只有被系统分配资源才能运行，运行状态的程序就是一个进程
程序是指令和数据的描述文本，是实物，进程是程序运行的一个状态，属于动态概念




"""

"""
迭代器；
迭代时是访问集合元素的方式，
迭代器从集合的第一个元素开始访问 一直都所有的元素都被访问一遍后结束

迭代器可以理解为是一个容器对象，他又两个基本的方法
next  返回容器的下一个元素
iter  返回迭代器本身

"""

"""
装饰器：

装饰器的作用是 在不改变原代码的情况下 为函数增加一些额外的功能
装饰器通常用于 数据校验 缓存  日志 性能测试

有了装饰器  我们可以抽离出大量于函数功能无关的大量代码进行复用

"""

# import time 

# def test_time(func):
#     def inner(*args,**kwargs):
#         strat_time = time.time()
#         func(*args,**kwargs)
#         stop_time = time.time()
#         print("运行时间为：%s"%(stop_time-strat_time))
#     return inner

# @test_time
# def func():
#     time.sleep(2)
#     print('hellow')

# func()

"""
生成器：
在python中 一边遍历 一遍计算的机制就是生成器
生成器会生成一系列的值 用于迭代，这样看它又是一种可迭代对象被。它是在for循环的过程中，不断的计算下一个元素，并在适当的条件下结束for循环

"""

"""
get
formkeys
pop
update
dick(zip(啊，b))
clear
setdefault
"""

"""
字段优化  尽量的遵循mysql的三范式
适当的使用 索引 因为索引会消耗内存空间 并不是越多越好
引擎的选择  适应的选择mylsam innedb
查询缓存   讲select的查询结果缓存起来  key为sql语句 val为查询结果 
分区 
集群
服务器的选择


"""


# def Fei(n):
#     num1,num2 = 0,1
#     current = 0
#     while current < n:
#         num = num1
#         num1,num2 = num2,num1+num2
#         current += 1
#         yield num
# if __name__ == "__main__":
#     ret = Fei(10)
#     for i in ret:
#         print(i)


"""
find

replace
split
join
strip


"""




# def Fei(n):

#     num1,num2 = 0,1
#     current = 0
#     while current < n:
#         num = num1
#         num1,num2 = num2,num1+num2
#         current += 1
#         yield num
# if __name__ == "__main__":
#     ret = Fei(10)
#     for i in ret:
#         print(i)


# import re

# ret = re.match(r"^1[3456789]\d{9}",'12212344321')

# if ret:
#     print('ok')
# else:
#     print('no')
import json

a_str = "[1,2,3]"
print(list(a_str))
a_str = eval(a_str)
print(a_str)