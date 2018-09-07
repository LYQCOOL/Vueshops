# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/17 19:37'
import xadmin
from  xadmin import views

from .models import *


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title='购物网后台管理'
    site_footer='七七大公司'
    menu_style='accordion'


class VerifyCodeAdmin(object):
    list_display=['code','mobile','add_time']
    search_fields=['code','mobile']
    list_filter=['code','mobile']

xadmin.site.register(VerifyCode,VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)