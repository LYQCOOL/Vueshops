"""Vueshops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import url, include
import xadmin
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from Vueshops.settings import MEDIA_ROOT
from goods.view_base import GoodsView
from goods.views import GoodsListViewSet, CategoryViewSet,BannerViewset,IndexCategoryViewset
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from trade.views import ShoppingCarViewset, OrderViewset, AlipayView

router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name='goods')
# 配置category的url
router.register(r'categorys', CategoryViewSet, base_name='categorys')
# 配置users验证码的url
router.register(r'codes', SmsCodeViewset, base_name='codes')
# 配置users注册的url
router.register(r'users', UserViewset, base_name='users')
# 配置收藏功能的url
router.register(r'userfavs', UserFavViewset, base_name='userfav')
# 配置留言功能的url
router.register(r'messages', LeavingMessageViewset, base_name='messages')
# 配置地址功能的url
router.register(r'address', AddressViewset, base_name='address')
# 配置购物车的url
router.register(r'shopcarts', ShoppingCarViewset, base_name='shopcarts')
# 配置订单相关的url
router.register(r'orders', OrderViewset, base_name='orders')
# 配置轮播图相关的url
router.register(r'banners', BannerViewset, base_name='banners')
# 配置商品系列数据
router.register(r'indexgoods', IndexCategoryViewset, base_name='indexgoods')

# 配置GoodsListViewSet
# good_list=GoodsListViewSet.as_view({
#         'get':'list',
#     })

urlpatterns = [
    # url('^admin/$', admin.site.urls),
    url('^xadmin/', xadmin.site.urls),
    # 配置文件及图片上传路径
    url('^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 配置drf文档
    url('^docs/', include_docs_urls(title='生鲜')),
    # url('^good/$',GoodsView.as_view(),name='good_'),
    #  url('^goods/$',good_list,name='good_list'),
    url('^', include(router.urls)),
    # drf登录配置
    url(r'^api-auth/', include('rest_framework.urls')),
    # drf自带的认证模式（Token）
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt的认证接口
    url(r'^login/$', obtain_jwt_token),
    # 支付接口url
    url(r'^alipay/return/', AlipayView.as_view(), name='alipay'),
    #配置template的url
    url(r'^index/$',TemplateView.as_view(template_name='index.html'),name='index'),
    url('', include('social_django.urls', namespace='social'))

]
