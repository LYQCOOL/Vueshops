# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/21 20:15'
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User=get_user_model()
#通过信号接收修改用户密码，加密
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        password=instance.password
        instance.set_password(password)
        instance.save()
