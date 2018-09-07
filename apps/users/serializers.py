# _*_ encoding:utf-8 _*_
import re
from datetime import datetime
from datetime import timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from Vueshops.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    '''
    注册手机号和验证码序列化
    '''
    mobile = serializers.CharField(max_length=11,min_length=11)

    def validate_mobile(self, mobile):
        '''
        验证手机号码
        '''
        # 验证手机是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号非法')
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')
        on_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=on_minute_ago, mobile=mobile):
            raise serializers.ValidationError('距离上一次发送未超过60秒')
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册序列化
    '''
    # write_only=True,不会拿该字段来序列化,labe标签名，help_text：docs文档中description
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label='验证码',
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "验证码不能为空",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },help_text='验证码')
    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已经存在')])
    #style密文,write_only=True不返回,保存为明文
    password = serializers.CharField(style={"input_type":"password"},write_only=True)
    #重载create函数，保存为密文,该方法可以实现加密密码，还可以信号（分离性好）
    # def create(self, validated_data):
    #     user=super(UserRegSerializer,self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_code(self, code):
        # 不用get，如果返回两条数据以上，会抛异常
        # try:
        #   verify_codes=VerifyCode.objects.get(mobile=self.initial_data['username'])
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass
        verify_codes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_codes:
            last_verfycode = verify_codes[0]
            five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minute_ago > last_verfycode.add_time:
                raise serializers.ValidationError('验证码过期')
            if code != last_verfycode.code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    # 作用于所有字段
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    用户详情页序列化类
    '''
    class Meta:
        model=User
        fields=('name','birthday','gender','email','mobile')


