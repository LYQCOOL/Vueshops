# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/13 15:21'
import json

from django.views.generic.base import View
from django.http import HttpResponse,JsonResponse
from .models import *


class GoodsView(View):
    def get(self,request):
       good_list=Goods.objects.all()[:10]
       datas=[]
       # for good in good_list:
       #     json_dict = {}
       #     json_dict['name']=good.name
       #     json_dict['goods_desc']=good.goods_desc
       #     json_dict['category']=good.category.name
       #     json_dict['shop_price']=good.shop_price
       #     #时间不是json序列化的对象
       #     json_dict['time']=good.add_time
       #     datas.append(json_dict)
       #直接序列化
       from django.forms.models import model_to_dict
       #用来做序列化
       from django.core import serializers
       datas=[]
       for good in good_list:
           #image和datetime不能序列化
          data=model_to_dict(good)
          datas.append(data)
       datas=serializers.serialize('json',good_list)
       datas=json.loads(datas)
       # return HttpResponse(datas,content_type='application/json')
       return JsonResponse(datas,safe=False)