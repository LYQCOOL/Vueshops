from datetime import datetime
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins
from rest_framework.views import APIView
from django.shortcuts import redirect

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCarSerializer, ShoppingCarDetailSerializer, OrderSerializer, OrderDetaiSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
from utils.alipay import AliPay
from Vueshops.settings import ali_pub_path, private_key_path


# Create your views here.


class ShoppingCarViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
       列出购物详情
    create:
       加入购物车
    update:
       更新购物车
    delete：
       删除购物车商品
    
    """
    serializer_class = ShoppingCarSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCarDetailSerializer
        else:
            return ShoppingCarSerializer

    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.filter(id=serializer.instance.id)
        existed_nums = existed_record.goods_num
        saved_record = serializer.save()
        num = saved_record.goods_num - existed_nums
        goods = saved_record.goods
        goods.goods_num -= num
        goods.save()


class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    '''
    list:
       列出订单详情
    create:
       创建订单
    destroy:
       删除订单
    '''
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetaiSerializer
        else:
            return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_good = OrderGoods()
            order_good.goods = shop_cart.goods
            order_good.goods_num = shop_cart.nums
            order_good.order = order
            order_good.save()
            shop_cart.delete()
        return order


class AlipayView(APIView):
    '''
    支付宝接口
    '''

    def get(self, request):
        '''
        处理return_url返回
        :param request: 
        :return: 
        '''
        process_dic = {}
        for key, value in request.GET.items():
            process_dic[key] = value
        sign = process_dic.pop('sign', None)
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

        verify_re = alipay.verify(process_dic, sign)
        if verify_re is True:
            order_sn = process_dic.get('order_sn', None)
            trade_no = process_dic.get('trade_no', None)
            trade_status = process_dic.get('trade_status', None)
            exsisted_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for exsisted_order in exsisted_orders:
                #销量数目修改
                order_goods=exsisted_order.objects.all()
                for order_good in order_goods:
                    goods=order_good.goods()
                    goods.sold_num+=order_good.goods_num
                    goods.save()
                exsisted_order.pay_status = trade_status
                exsisted_order.trade_no = trade_no
                exsisted_order.pay_time = datetime.now()
                exsisted_order.save()

        return Response("success")

    def post(self, request):
        '''
        处理notify_url
        :param request: 
        :return: 
        '''
        process_dic = {}
        for key, value in request.POST.items():
            process_dic[key] = value
        sign = process_dic.pop('sign', None)
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

        verify_re = alipay.verify(process_dic, sign)
        if verify_re is True:
            order_sn = process_dic.get('order_sn', None)
            trade_no = process_dic.get('trade_no', None)
            trade_status = process_dic.get('trade_status', None)
            exsisted_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for exsisted_order in exsisted_orders:
                exsisted_order.pay_status = trade_status
                exsisted_order.trade_no = trade_no
                exsisted_order.pay_time = datetime.now()
                exsisted_order.save()
                # 配置index跳转
            response = redirect('index')
            response.set_cookie('nextPath', 'pay', max_age=2)
            return response
        else:
            response = redirect('index')
            return response
            # return Response("success")
