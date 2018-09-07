import re

from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator
from goods.serializers import GoodsSerializer

from .models import UserFav, UserLeavingMessage, UserAddress
from Vueshops.settings import REGEX_MOBILE


class UserFavSerializer(serializers.ModelSerializer):
    # user默认为当前user，字段隐藏
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        # 删除返回id
        # 配置两个字段联合唯一，收藏功能，models中 unique_together = ("user", "goods")，可以不用配置
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='已经收藏'
            )
        ]
        fields = ('user', 'goods', 'id')


class UserFavDetaiSerializer(serializers.ModelSerializer):
    '''
    用户收藏详情序列化
    '''
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    '''
    留言序列化
    '''
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'message_type', 'subject', 'message', 'file', 'id', 'add_time')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    signer_mobile = serializers.CharField(required=True, max_length=11, min_length=11, label='电话',
                                          error_messages={"max_length": "请填写正确的手机号", "min_length": "请填写正确的手机号"},
                                          help_text='电话')
    province = serializers.CharField(required=True, label='省份')
    city = serializers.CharField(required=True, label="城市")
    district = serializers.CharField(required=True, label="区域")
    signer_name = serializers.CharField(required=True, min_length=2, max_length=4, label="签收人",
                                         error_messages={"min_length": "签收人名字应该在两到四个字符之间",
                                                         "max_length": "签收人名字应该在两到四个字符之间",
                                                         "requires": "签收人不能为空"})
    address = serializers.CharField(required=True, label="详细地址")

    class Meta:
        model = UserAddress
        fields = ("__all__")

    def validate_mobile(self, signer_mobile):
        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError('手机号不合法，请查看是否填写正确')
        return signer_mobile
