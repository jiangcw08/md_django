import requests

#定义上传的文件  文件名，文件实体
files = {'file':('touxiang.png',open('D:\\tu\\1.png','rb'))}

#发起请求
res = requests.post('http://localhost:8000/file/',files=files)

print(res.text)

