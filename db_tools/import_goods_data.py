# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/17 19:30'

#独立使用django的model
import sys
import os


pwd=os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+'../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vueshops.settings")

import django
django.setup()
#位置要放对，配置好引入
from goods.models import Goods,GoodsCategory,GoodsImage
from db_tools.data.product_data import row_data

for good_detail in row_data:
    good_instance=Goods()
    good_instance.market_price=float(int(good_detail['market_price'].replace('￥','').replace('元','')))
    good_instance.name=good_detail['name']
    good_instance.good_desc=good_detail['goods_desc'] if good_detail['goods_desc'] is not None else ''
    good_instance.shop_price=float(int(good_detail['sale_price'].replace('￥','').replace('元','')))
    good_instance.goods_brief=good_detail['desc'] if good_detail['desc'] is not None else ''
    good_instance.goods_front_image=good_detail['images'][0] if good_detail['images'] else ''
    category_name=good_detail['categorys'][-1]
    category=GoodsCategory.objects.filter(name=category_name).first()
    if category:
        good_instance.category=category
        good_instance.save()
    for good_image in good_detail['images']:
        good_image_instance=GoodsImage()
        good_image_instance.goods=good_instance
        good_image_instance.image=good_image
        good_image_instance.save()