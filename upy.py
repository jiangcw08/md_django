import upyun

#新建又拍云 实列



up = upyun.UpYun('jiangcw-upyun','jiangcw','Tb5WxPjiIpklrG6heUZSwb15SnIQ5ETv')

#上传文件
# up.put(('/test.txt','hellow_upyun\nhellow_word'))


#文件流操作(节省内存)
# with open('./jay1.jpg','rb') as f:
#     #上传
#     res = up.put('/upy_test.png',f,checksum=True)

#目录操作
# up.mkdir('/meiduo/')

#移动文件
# up.move('/test.txt','/meiduo/test2.txt')

#复制文件
# up.copy('/meiduo/test2.txt','/meiduo/test3.txt')


#断点续传
# with open('c:/test.MP4','rb') as f:
#     res = up.put('/meiduo/test.mp4',f,checksum=True,need_resume=True)


# #下载
# res = up.get('/meiduo/test2.txt')
# print(res)

#删除文件
up.delete('/meiduo/test2.txt')
