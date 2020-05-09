from rest_framework.views import Response,APIView

#又拍云存储
import upyun
class UploadUpy(APIView):

    def post(self,request):

        #获取文件
        file = request.FILES.get('file')
        #新建又拍云实例
        up = upyun.UpYun('jiangcw-upyun','jiangcw','Tb5WxPjiIpklrG6heUZSwb15SnIQ5ETv')
        #声明头部信息
        headers = {'x-gmkerl-rotate':'auto'}
        #上传图片
        for chunk in file.chunks():
            res = up.put(file.name,chunk,checksum=True,headers=headers)
        return Response({'filename':file.name})

class Mkdir(APIView):

    def get(self,request):

        name = request.GET.get('name')


        up = upyun.UpYun('jiangcw-upyun','jiangcw','Tb5WxPjiIpklrG6heUZSwb15SnIQ5ETv')
        up.mkdir(name)

        return Response({'code':200,'message':'创建成功'})

class Del(APIView):

    def get(self,request):


        name = request.GET.get('name')

        up = upyun.UpYun('jiangcw-upyun','jiangcw','Tb5WxPjiIpklrG6heUZSwb15SnIQ5ETv')
        up.delete(name)
        return Response({'code':200,'message':'ok'})