# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/18 17:52'

from rest_framework import serializers
from django.db.models import Q

from goods.models import *


# form对应:Serializer,modelform:ModelSerializer
# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True,max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image=serializers.ImageField()
#     add_time=serializers.DateTimeField()
#
#     def create(self, validated_data):
#         return Goods.objects.create(**validated_data)

# 嵌套商品列表页（三层）
class GoodsCategorySerializer3(serializers.ModelSerializer):
    '''
    商品类别序列化
    '''

    class Meta:
        model = GoodsCategory
        fields = ('__all__')


class GoodsCategorySerializer2(serializers.ModelSerializer):
    '''
    商品类别序列化
    '''
    sub_cat = GoodsCategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = ('__all__')


class GoodsCategorySerializer(serializers.ModelSerializer):
    '''
    商品类别序列化
    '''
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = ('__all__')


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    # 替换默认的category
    category = GoodsCategorySerializer()
    # 可能有多条many=True
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        # fields=('name','click_num','market_price','add_time','goods_front_image')
        # 外键为id,想要完整信息，嵌套Serializer
        fields = ('__all__')


class BannerSerializer(serializers.ModelSerializer):
    '''
    轮播图序列化
    '''

    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    '''
    品牌序列化
    '''

    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class IndexCategorySerializer(serializers.ModelSerializer):
    '''
    商品分类序列化
    '''
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = GoodsCategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id, )
        if ad_goods:
            good_ins = ad_goods[0].goods
            # 在serializer中调用seria不会把图片路劲自动补充完整，需要加上参数context={'request': self.context['request']}
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'
