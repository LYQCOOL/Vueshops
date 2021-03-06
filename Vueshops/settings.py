"""
Django settings for Vueshops project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k35)k0%+kkif-+r-zw+!j3qa-hu!*4y9vodgl%a=^)39ly#@px'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL='users.UserProfile'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'user_operation',
    'trade',
    'goods',
    'xadmin',
    'crispy_forms',
    'DjangoUeditor',
    'rest_framework',
    #筛选器
    'django_filters',
    #跨域
    'corsheaders',
    #Token验证，会生成表
    'rest_framework.authtoken',
    #第三方登录
    'social_django'

]

MIDDLEWARE = [
    #跨域，放在CsrfViewMiddleware之前
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#跨域
CORS_ORIGIN_ALLOW_ALL=True
ROOT_URLCONF = 'Vueshops.urls'
STATICFILES_DIRS=(
    os.path.join(BASE_DIR,'static'),
                  )

AUTHENTICATION_BACKENDS=(
  'users.views.CustomBackend',
  #第三方登录
  'social_core.backends.weibo.WeiboOAuth2',
  'social_core.backends.qq.QQOAuth2',
  'social_core.backends.weixin.WeixinOAuth2',
  'django.contrib.auth.backends.ModelBackend',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #第三方登录配置
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'Vueshops.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vueshop',
        'USER': 'root',
        'PASSWORD': '112358',
        'HOST': 'localhost',
        'PORT': '3306',
         #mysql engine有两种，默认为MyISAM，还有INNODB,版本不同，有的是storage_engine
        'OPTIONS':{'init_command':'SET default_storage_engine=INNODB;'}
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')

#所有rest_framework配置
# REST_FRAMEWORK={
#     'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE':5
# }
#登录
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        #如果Token过期，不需要登录的界面也不能访问，最好配置在具体的页面
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',

),
    #throttle限速ip(防爬虫对服务器的压力)
    'DEFAULT_THROTTLE_CLASSES': (
        #未登录状态
        'rest_framework.throttling.AnonRateThrottle',
        #登录状态
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
import datetime
JWT_AUTH={
    #Token失效时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    #Token前缀
    'JWT_AUTH_HEADER_PREFIX': 'JWT'
}
#手机号码正则表达式
REGEX_MOBILE='^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$'
#云片apikey
APIKEY='d97d7caf968b3f5ec56fb2a2488140b6'
#缓存时间失效设置
REST_FRAMEWORK_EXTENSIONS={
'DEFAULT_CACHE_RESPONSE_TIMEOUT':100
}
#配置redis缓存
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }
#支付宝相关配置apipay
private_key_path=os.path.join(BASE_DIR,'apps/trade/keys/private_2048.txt')
ali_pub_path=os.path.join(BASE_DIR,'apps/trade/keys/alipay_key_2048.txt')
#配置第三方登录的client_id和client_secret
SOCIAL_AUTH_WEIBO_KEY = '3993500018'
SOCIAL_AUTH_WEIBO_SECRET = '255a336de9c48c756ea464f9339dea27'

SOCIAL_AUTH_QQ_KEY = 'jFBcq3gvcDVCBuGM'
SOCIAL_AUTH_QQ_SECRET = '1107728425'

SOCIAL_AUTH_WEIXIN_KEY = 'foobar'
SOCIAL_AUTH_WEIXIN_SECRET = 'bazqux'
#配置登录成功跳转页面
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'


