"""
Django settings for fir_ser project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from celery.schedules import crontab

from config import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = BASECONF.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = BASECONF.DEBUG

ALLOWED_HOSTS = BASECONF.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'rest_framework',
    'captcha',
    'django_celery_beat',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.utils.middlewares.CorsMiddleWare'
]

ROOT_URLCONF = 'fir_ser.urls'

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

WSGI_APPLICATION = 'fir_ser.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DBCONF.name,
        'USER': DBCONF.user,
        'PASSWORD': DBCONF.password,
        'HOST': DBCONF.host,
        'PORT': DBCONF.port,
        # 设置MySQL的驱动
        # 'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},
        'OPTIONS': {'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"', 'charset': 'utf8mb4'}
    }

}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'api.utils.throttle.LoginUserThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': BASECONF.DEFAULT_THROTTLE_RATES
}
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# Media配置
MEDIA_URL = "files/"
MEDIA_ROOT = os.path.join(BASE_DIR, "files")
# supersign配置
SUPER_SIGN_ROOT = os.path.join(BASE_DIR, "supersign")

AUTH_USER_MODEL = "api.UserInfo"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%s/1" % (CACHECONF.host, CACHECONF.port),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": CACHECONF.password,
            "DECODE_RESPONSES": True
        },
        "TIMEOUT": 60 * 15
    },
}

# DRF扩展缓存时间
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 3600,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}
# 取消自动加斜杠
APPEND_SLASH = False

# geetest 配置信息
GEETEST_ID = BASECONF.GEETEST_ID
GEETEST_KEY = BASECONF.GEETEST_KEY
GEETEST_CYCLE_TIME = BASECONF.GEETEST_CYCLE_TIME
GEETEST_BYPASS_STATUS_KEY = BASECONF.GEETEST_BYPASS_STATUS_KEY
GEETEST_BYPASS_URL = BASECONF.GEETEST_BYPASS_URL

# 注册方式，如果启用sms或者email 需要配置 THIRD_PART_CONFIG_KEY_INFO.sender 信息
REGISTER = AUTHCONF.REGISTER
# 个人资料修改修改也会使用该配置
CHANGER = AUTHCONF.CHANGER
LOGIN = AUTHCONF.LOGIN
REPORT = AUTHCONF.REPORT
THIRD_PART_CONFIG_KEY_INFO = {
    # APP存储配置
    'storage_key': STORAGEKEYCONF.STORAGE,
    'sender_key': SENDERCONF.SENDER
}
CACHE_KEY_TEMPLATE = {
    'user_can_download_key': 'user_can_download',
    'download_times_key': 'app_download_times',
    'make_token_key': 'make_token',
    'download_short_key': 'download_short',
    'app_instance_key': 'app_instance',
    'download_url_key': 'download_url',
    'user_storage_key': 'storage_auth',
    'user_auth_token_key': 'user_auth_token',
    'download_today_times_key': 'download_today_times',
    'developer_auth_code_key': 'developer_auth_code',
    'upload_file_tmp_name_key': 'upload_file_tmp_name',
    'login_failed_try_times_key': 'login_failed_try_times',
    'user_free_download_times_key': 'user_free_download_times',
    'super_sign_failed_send_msg_times_key': 'super_sign_failed_send_msg_times',
    'wx_access_token_key': 'wx_basic_access_token',
    'wx_ticket_info_key': 'wx_ticket_info',
    'ipa_sign_udid_queue_key': 'ipa_sign_udid_queue',
}

DATA_DOWNLOAD_KEY = "d_token"
FILE_UPLOAD_TMP_KEY = ".tmp"
USER_FREE_DOWNLOAD_TIMES = 5
AUTH_USER_FREE_DOWNLOAD_TIMES = 10
NEW_USER_GIVE_DOWNLOAD_TIMES = 100
AUTH_USER_GIVE_DOWNLOAD_TIMES = 200

SYNC_CACHE_TO_DATABASE = {
    'download_times': 10,  # 下载次数同步时间
    'wx_get_access_token_times': 60 * 10,  # 微信access_token 自动获取时间
    'try_login_times': (10, 12 * 60 * 60),  # 当天登录失败次数，超过该失败次数，锁定24小时
    'auto_clean_tmp_file_times': 60 * 30,  # 定时清理上传失误生成的临时文件
    'auto_clean_local_tmp_file_times': 60 * 30,  # 定时清理临时文件,现在包含超级签名描述临时文件
    'try_send_msg_over_limit_times': (3, 60 * 60),  # 每小时用户发送信息次数
    'clean_local_tmp_file_from_mtime': 60 * 60,  # 清理最后一次修改时间超过限制时间的临时文件,单位秒
    'auto_check_ios_developer_active_times': 60 * 60 * 12,  # ios开发者证书检测时间
}

SERVER_DOMAIN = BASECONF.SERVER_DOMAIN

MOBILE_CONFIG_SIGN_SSL = IPACONF.MOBILE_CONFIG_SIGN_SSL

DEFAULT_MOBILEPROVISION = IPACONF.DEFAULT_MOBILEPROVISION
# DEFAULT_MOBILEPROVISION = {
#     # 默认描述文件路径或者下载路径，用户企业签名或者超级签名 跳转 [设置 - 通用 - 描述文件|设备管理] 页面
#     # 如果配置了path路径，则走路径，如果配置了url，则走URL，path 优先级大于url优先级
#     'enterprise': {
#         'path': os.path.join(MEDIA_ROOT, 'embedded.mobileprovision'),
#         'url': 'https://ali-static.jappstore.com/embedded.mobileprovision'
#     },
#     'supersign': {
#         # 超级签名，如果self 为True，则默认用自己的描述文件，否则同企业配置顺序一致,自己的配置文件有时候有问题
#         'self': False,
#         'path': os.path.join(MEDIA_ROOT, 'embedded.mobileprovision'),
#         'url': 'https://ali-static.jappstore.com/embedded.mobileprovision'
#     }
# }

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CAPTCHA_TIMEOUT = 5  # Minutes
CAPTCHA_LENGTH = 6  # Chars

BASE_LOG_DIR = os.path.join(BASE_DIR, "logs", "flyapp")
if not os.path.isdir(BASE_LOG_DIR):
    os.makedirs(BASE_LOG_DIR)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'TF': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，根据时间自动切
            'filename': os.path.join(BASE_LOG_DIR, "flyapp_info.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
            'backupCount': 10,  # 备份数为3  xx.log --> xx.log.2018-08-23_00-00-00 --> xx.log.2018-08-24_00-00-00 --> ...
            # 'when': 'W6',  # 每天一切， 可选值有S/秒 M/分 H/小时 D/天 W0-W6/周(0=周一) midnight/如果没指定时间就默认在午夜
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "flyapp_err.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
            'backupCount': 10,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "flyapp_warning.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
            'backupCount': 10,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'pay': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "flyapp_pay.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
            'backupCount': 10,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {  # 默认的logger应用如下配置
            'handlers': ['TF', 'console', 'error', 'warning'],  # 上线之后可以把'console'移除
            'level': 'DEBUG',
            'propagate': True,
        },
        'pay': {  # 默认的logger应用如下配置
            'handlers': ['pay'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

PAY_CONFIG_KEY_INFO = PAYCONF.PAY_CONFIG_KEY_INFO

# 结果存放到Django|redis
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'django-cache'
# result_backend = 'redis://username:password@host:port/db'
# result_backend = 'redis://:password@host:port/db'
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'


# broker redis|mq
DJANGO_DEFAULT_CACHES = CACHES['default']
CELERY_BROKER_URL = 'redis://:%s@%s/2' % (
    DJANGO_DEFAULT_CACHES["OPTIONS"]["PASSWORD"], DJANGO_DEFAULT_CACHES["LOCATION"].split("/")[2])
# CELERY_BROKER_URL = 'amqp://guest@localhost//'
#: Only add pickle to this list if your broker is secured


CELERY_WORKER_CONCURRENCY = 30  # worker并发数
CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死
CELERY_RESULT_EXPIRES = 3600  # 任务结果过期时间

CELERY_WORKER_DISABLE_RATE_LIMITS = True  # 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
CELERY_WORKER_PREFETCH_MULTIPLIER = 60  # celery worker 每次去redis取任务的数量

CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000  # 每个worker执行了多少任务就会死掉，我建议数量可以大一些，比如200

CELERY_ENABLE_UTC = False
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'sync_download_times_job': {
        'task': 'api.tasks.sync_download_times_job',
        'schedule': SYNC_CACHE_TO_DATABASE.get("download_times"),
        'args': ()
    },
    'check_bypass_status_job': {
        'task': 'api.tasks.check_bypass_status_job',
        'schedule': GEETEST_CYCLE_TIME,
        'args': ()
    },
    'auto_clean_upload_tmp_file_job': {
        'task': 'api.tasks.auto_clean_upload_tmp_file_job',
        'schedule': SYNC_CACHE_TO_DATABASE.get("auto_clean_tmp_file_times"),
        'args': ()
    },
    'auto_delete_tmp_file_job': {
        'task': 'api.tasks.auto_delete_tmp_file_job',
        'schedule': SYNC_CACHE_TO_DATABASE.get("auto_clean_local_tmp_file_times"),
        'args': ()
    },
    'auto_check_ios_developer_active_job': {
        'task': 'api.tasks.auto_check_ios_developer_active_job',
        # 'schedule': SYNC_CACHE_TO_DATABASE.get("auto_check_ios_developer_active_times"),
        'schedule': crontab(hour=1, minute=1),
        'args': ()
    },
    # 'start_api_sever_do_clean': {
    #     'task': 'api.tasks.start_api_sever_do_clean',
    #     'schedule': 6,
    #     'args': (),
    #     'one_off': True
    # },
    'sync_wx_access_token_job': {
        'task': 'api.tasks.sync_wx_access_token_job',
        'schedule': SYNC_CACHE_TO_DATABASE.get("wx_get_access_token_times"),
        'args': (),
    },
}

MSGTEMPLATE = {
    'NOT_EXIST_DEVELOPER': '用户 %s 你好，应用 %s 签名失败了，苹果开发者总设备量已经超限，请添加新的苹果开发者或者修改开发者设备数量。感谢有你!',
    'ERROR_DEVELOPER': '用户 %s 你好，应用 %s 签名失败了，苹果开发者 %s 信息异常，请重新检查苹果开发者状态是否正常。感谢有你!',
    'AUTO_CHECK_DEVELOPER': '用户 %s 你好，苹果开发者 %s 信息异常，请重新检查苹果开发者状态是否正常。感谢有你!',
}

## listen port

SERVER_BIND_HOST = BASECONF.SERVER_BIND_HOST
SERVER_LISTEN_PORT = BASECONF.SERVER_LISTEN_PORT
CELERY_FLOWER_PORT = BASECONF.CELERY_FLOWER_PORT
CELERY_FLOWER_HOST = BASECONF.CELERY_FLOWER_HOST
