# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/19 10:07'

import django_filters
from django.db.models import Q

from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    #help_text--docs：description
    pricemin=django_filters.NumberFilter(field_name='shop_price',lookup_expr='gte',help_text='最低价格')
    pricemax=django_filters.NumberFilter(field_name='shop_price',lookup_expr='lte')
    # name=django_filters.CharFilter(field_name='name',lookup_expr='icontains')
    top_category=django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self,queryset,name,value):
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))


    class Meta:
        model=Goods
        fields=['pricemin','pricemax','top_category','is_hot','is_new']