from rest_framework.views import Response,APIView
from myapp.models import Goods
from django.db.models import Q
from myapp.myser import GoodsSer




#商品列表
class Get_goods(APIView):
    def get(self,request):

        #检索字段
        text = request.GET.get('text',None)

        #获取当前页
        page = request.GET.get('page',1)
        #一页显示个数
        size = request.GET.get('size',2)
        #计算从哪切
        data_start = (int(page)-1) * int(size)
        #计算切到哪
        data_end = int(page) * int(size)

        

        #查询 切片操作
        goods = Goods.objects.all()[data_start:data_end]

        #是否进行模糊查询
        if text:

            goods = Goods.objects.filter(Q(name__contains=text) | Q(desc__contains=text))[data_start:data_end]

            count = Goods.objects.filter(Q(name__contains=text) | Q(desc__contains=text)).count()

        else:

        #查询所有商品个数
            count = Goods.objects.count()

        goods_ser = GoodsSer(goods,many=True)

        res = {}
        res['total'] = count
        res['data'] = goods_ser.data

        return Response(res)