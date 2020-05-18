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

import request
import redis
#定义地址和端口
host = '127.0.0.1'
port = 6379
