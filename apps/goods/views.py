from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
#缓存
from rest_framework_extensions.cache.mixins import CacheResponseMixin
#ip限制访问次数
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

from .filters import GoodsFilter
from .models import *
from .serializers import GoodsSerializer,GoodsCategorySerializer,BannerSerializer,IndexCategorySerializer

#基于APIView
'''class GoodsListView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)

    def post(self,request,format=None):
        serializer=GoodsSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(request.data,status=status.HTTP_201_CREATED)
        return Response(request.data,status=status.HTTP_400_BAD_REQUEST)'''

#基于mixins,必须重载get函数
# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
#     """
#     商品详情页
#     """
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


#深度定制分页
class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


#直接继承ListAPIView,不用重写get函数
# class GoodsListView(generics.ListAPIView):
#     """
#     商品详情页
#     """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     #分页
#     pagination_class = GoodsPagination
#
#     # def get(self, request, *args, **kwargs):
#     #     return self.list(request, *args, **kwargs)


#更好的View:viewsets.GenericViewSet
# class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
#     """
#     商品详情页
#     """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     #分页
#     pagination_class = GoodsPagination
#     def get_queryset(self):
#
#         # min_price = self.request.query_params.get('price_min',0)
#         # if min_price:
#         #     queryset=queryset.filter(shop_price__gt=int(min_price))
#         return Goods.objects.filter(shop_price__gt=100).order_by('shop_price')


#基于django_filter过滤数据
#可以根据id查看详情页mixins.RetrieveModelMixin
class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    商品详情页，分页，搜索，过滤，排序
    """
    #配置ip限制访问次数
    throttle_classes = (UserRateThrottle,AnonRateThrottle)
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    #分页
    pagination_class = GoodsPagination
    #配置认证类，防止公开网页（未登录可查看）不能访问
    # authentication_classes = (TokenAuthentication,)
    filter_backends=(DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    #字段过滤(DjangoFilterBackend)
    # filter_fields = ('name', 'shop_price')
    filter_class=GoodsFilter
    #搜索过滤（rest_framework.filters.SearchFilter）
    search_fields = ('name','goods_brief','goods_desc')
    #排序过滤(rest_frameworkfilters.OrderingFilter)
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num+=1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    list:
        商品列表页
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    ''''
    list:
       轮播图展示
    '''
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    list:
       首页商品分页数据
    '''
    queryset = GoodsCategory.objects.filter(is_tab=True)
    serializer_class = IndexCategorySerializer




