import time
import random

from rest_framework import serializers

from .models import Goods, ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer
from Vueshops.settings import private_key_path, ali_pub_path
from utils.alipay import AliPay


class ShoppingCarSerializer(serializers.Serializer):
    '''
    购物车序列化
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, min_value=1, label='数量',
                                    error_messages={
                                        "requires": "请选择商品数量",
                                        "min_value": "商品数量不能小于1"
                                    })
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True, label='商品')

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        '''
        修改商品数量
        :param instance: 
        :param validated_data: 
        :return: 
        '''
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class ShoppingCarDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    '''
    订单序列化
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        '''
        生成url
        :return: 
        '''
        alipay = AliPay(
            # 沙箱环境appid
            appid="2016091800536621",
            app_notify_url="http://47.106.211.59:8008/alipay/return/",
            # 私钥路径
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.106.211.59:8008/alipay/return/"
        )
        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            # return_url="http://47.106.211.59:8008/alipay/return/"
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"

    def generate_order_sn(self):
        # 生成订单号（当前时间加用户id加随机数）
        random_ins = random.Random()
        order_sn = "{timestr}{userid}{ranstr}".format(timestr=time.strftime("%Y%m%d%H%M%S"),
                                                      userid=self.context['request'].user.id,
                                                      ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetaiSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        '''
        生成url
        :return: 
        '''
        alipay = AliPay(
            # 沙箱环境appid
            appid="2016091800536621",
            app_notify_url="http://47.106.211.59:8008/alipay/return/",
            # 私钥路径
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.106.211.59:8008/alipay/return/"
        )
        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            # return_url="http://47.106.211.59:8008/alipay/return/"
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"
