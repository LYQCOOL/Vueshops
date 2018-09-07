import random

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler

from Vueshops.settings import APIKEY
from .models import UserProfile,VerifyCode
from .serializers import SmsSerializer,UserRegSerializer,UserDetailSerializer
from utils.yunpian import YunPian
User=get_user_model()

# Create your views here.
class CustomBackend(ModelBackend):
   '''
   自定义用户验证(setting.py)
   '''
   def authenticate(self, username=None, password=None, **kwargs):
       try:
           user=UserProfile.objects.get(Q(username=username)|Q(mobile=username))
           user.check_password(password)
           return user
       except Exception as e:
           return None


class SmsCodeViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    '''
    云片网发送短信验证码接口
    '''
    serializer_class = SmsSerializer

    def generate_code(self):
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(random.choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile=serializer.validated_data['mobile']
        yun_pian=YunPian(APIKEY)
        code=self.generate_code()
        ssm_status=yun_pian.send_sms(code=code,mobile=mobile)
        if ssm_status['code']!=1:
            return Response({'mobile':ssm_status["msg"]},status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record=VerifyCode(code=code,mobile=mobile)
            code_record.save()
            return Response({'mobile': mobile},status=status.HTTP_201_CREATED)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    用户
    '''
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication)
    #更新，添加用户信息放在一起，是否登录应该动态，注册不用登录IsAuthenticated，该方法不行
    # permission_classes = (permissions.IsAuthenticated)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=self.perform_create(serializer)
        re_dict=serializer.data
        payload=jwt_payload_handler(user)
        re_dict['token']=jwt_encode_handler(payload)
        re_dict['name']=user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        '''
        重载GenericAPIView中的get_serializer_class函数，调用不同的序列化类，如果是create,
        就调用UserRegSerializer序列化，否则UserDetailSerializer序列化
        :return: 
        '''
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):
        '''
        重载APIview中的get_perimissions函数，如果是新增用户则不用登录，否则必须登录
        :return: 
        '''
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def get_object(self):
        '''
        返回当前用户
        :return: 
        '''
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


