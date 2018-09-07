# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/17 19:56'
import xadmin

from .models import *


class UserFavAdmin(object):
    list_display=['user','goods','add_time']
    search_fields=['user','goods']
    list_filter=['user','goods','add_time']


class UserLeavingMessageAdmin(object):
    list_display = ['user', 'message_type', 'subject','message','file','add_time']
    search_fields = ['user', 'message_type', 'subject','message','file']
    list_filter = ['user', 'message_type', 'subject','message','file','add_time']


class UserAddressAdmin(object):
    list_display = ['user', 'province', 'city', 'district', 'address', 'signer_name','signer_mobile','add_time']
    search_fields = ['user', 'province', 'city', 'district', 'address', 'signer_name','signer_mobile']
    list_filter = ['user', 'province', 'city', 'district', 'address', 'signer_name','signer_mobile','add_time']

xadmin.site.register(UserFav,UserFavAdmin)
xadmin.site.register(UserLeavingMessage,UserLeavingMessageAdmin)
xadmin.site.register(UserAddress,UserAddressAdmin)
