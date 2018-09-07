from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializers import UserFavSerializer, UserFavDetaiSerializer, LeavingMessageSerializer, AddressSerializer
from .models import UserFav, UserLeavingMessage, UserAddress
from utils.permissions import IsOwnerOrReadOnly


# Create your views here.
class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否收藏
    create:
        收藏商品
    '''
    # queryset = UserFav.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # serializer_class=UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 自己设置详情页搜索的id,默认为id
    lookup_field = 'goods_id'

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        '''
        重载GenericAPIView中的get_serializer_class函数，调用不同的序列化类，如果是create,
        就调用UserRegSerializer序列化，否则UserDetailSerializer序列化
        :return: 
        '''
        if self.action == "list":
            return UserFavDetaiSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer


    # def perform_create(self, serializer):
    #     '''
    #     重载CreateModelMixin中的函数实现收藏加一,也可用信号量实现（代码分离性好）
    #     :param serializer:
    #     :return:
    #     '''
    #     instance=serializer.save()
    #     goods=instance.goods
    #     goods.fav_num+=1
    #     goods.save()
    # def perform_destroy(self, instance):
    #        # 重载DestroyModelMixin中的函数实现收藏减一, 也可用信号量实现（代码分离性好）
    #         instance=instance.delete()
    #         goods=instance.goods
    #         goods.fav_num-=1
    #         goods.save()



class LeavingMessageViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    '''
    list:
       获取留言
    create:
       添加留言
    destroy:
       删除留言
    
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    '''
    所有的mixin都继承了
    收货地址管理
    list:
       获取收货地址
    create:
       添加收货地址
    update:
       更新收货地址
    delete:
    删除收货地址
    '''
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


