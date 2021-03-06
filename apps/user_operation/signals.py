# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/21 20:15'
from django.conf import settings
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from .models import UserFav


# 通过信号实现收藏加一
@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


# 通过信号实现收藏减一
@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
