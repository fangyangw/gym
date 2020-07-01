"""
Django settings for Fit project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vt&nh3%ggjaw9!_*%z9+73j&y!e=%_^mqb*7fe&@3^p4s+gfyd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Fitness.apps.FitnessConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_apscheduler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 跨域问题
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Fitness.utils.middleware.StartupMiddleware',
]

ROOT_URLCONF = 'Fit.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'Fit.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fit',
        'HOST': '101.132.117.242',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'Yujia123!',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'fitness',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'USER': 'root',
#         'PASSWORD': '123',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.BasicAuthentication',
                                       'rest_framework.authentication.SessionAuthentication',
                                       'rest_framework.authentication.TokenAuthentication'
                                       ],
    # 解决跨域问题
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny', ],
    # 默认使用的版本控制类
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    # 允许的版本
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    # 版本使用的参数名称
    'VERSION_PARAM': 'version',
    # 默认使用的版本
    'DEFAULT_VERSION': 'v1',
    # 配置全局认证
    # 'DEFAULT_AUTHENTICATION_CLASSES': ["ecolo_pro.utils.authentication.MyAuth", ]
}
# CORS
# CORS_ORIGIN_WHITELIST = (
#     '127.0.0.1:8080',
#     'localhost:8080',
#     'www.ezaifit.top:8080',
#     'www.ezaifit.top:8000',
#     'www.ezaifit.top:80',
#     'www.ezaifit.top:443'
# )
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie
# 凡是出现在白名单中的域名，都可以访问后端接口
# CORS_ALLOW_CREDENTIALS 指明在跨域访问中，后端是否支持对cookie的操作。

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)
# 微信配置
AppID = 'wx6e7157cd6dfbb4ec'
AppSecret = 'f62dcf502f8379c94323e774e877c714'
Token = ''
ROOT_URL = ''
verification_code_in_date = 5
#普通短信发送的URL
sms_send_uri = "http://smssh1.253.com:80/msg/send/json"
#创蓝API账号
sms_account = "N0725000"
#创蓝API密码
sms_password = "DaY9epzFjN19f3"

sms_template = "【易在24H健身】%s，是您的登录验证码，请在5分钟内按页面提示提交验证码，切勿泄露给他人，如非本人操作请忽略本短信。"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')
VIP_STATUS_COUNT_INTERVAL = 60 * 30 #60 * 2
ENABLE_SCHEDULER = True
IS_ON_SALE = True
FREE_DAY = 1

STATIC_URL = '/static/'
STATICFILES_DIR = [
    os.path.join(BASE_DIR,'static'),
]
STATIC_ROOT = '/usr/share/python/static'

YIBI_NUMBER_FROM_SHARE = 10

LANGUAGE_CODE = 'zh-Hans'

# Windows环境中此项的时区必须和系统一致，设置为 Asia/Shanghai。
# 另外此项设置如果保持 UTC 有可能导致 Django 时间和本地时间不同的情况。
# TIME_ZONE = 'Asia/Shanghai'
# 这里必须是 True，否则 LANGUAGE_CODE 会失效
USE_I18N = True
FREE_CARD_NAME = "7 day free for new user"
DISCOUNT_PRICE = [158, 128, 98]
DICCOUNT_REMARK = "连续包月卡首月158元，次月128元，以后每月98元"
FIRST_ORDER_REWARD_RATE = 0.1
NOTICE_DAY = 2
NOTICE_NAME = "会员卡"
NOTICE_REMARK = "请注意时间，防止过期"
# USE_TZ = False