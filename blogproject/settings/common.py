"""
Django settings for blogproject project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
back = os.path.dirname

BASE_DIR = back(back(back(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',  # install blog app
    'comments.apps.CommentsConfig',  # install comments app
    'userprofile.apps.UserprofileConfig',  # install userprofile app
    'password_reset',  # install password-reset module
    'mptt',  # install mptt module
    'ckeditor',  # install ckeditor module
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blogproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'blogproject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

# ?????????????????????????????????10??????
PASSWORD_RESET_TOKEN_EXPIRES = 60 * 10

# SMTP?????????????????????????????????smtp!
EMAIL_HOST = 'smtp.163.com'
# ??????????????????????????????
EMAIL_HOST_USER = 'mk180400112@163.com'
# ??????????????????
EMAIL_HOST_PASSWORD = 'RDLBFUYPCQRABJWR'
# ?????????????????????
EMAIL_PORT = 25
# ???????????? TLS
EMAIL_USE_TLS = True
# ??????????????????
DEFAULT_FROM_EMAIL = 'M010K????????? <mk180400112@163.com>'

CKEDITOR_CONFIGS = {
    # django-ckeditor????????????default??????
    'default': {
        # ????????????????????????
        'width': 'auto',
        'height': '250px',
        # tab??????????????????
        'tabSpaces': 4,
        # ???????????????
        'toolbar': 'Custom',
        # ???????????????
        'toolbar_Custom': [
            # ?????? ?????????
            ['Smiley', 'CodeSnippet'],
            # ????????????
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            # ????????????
            ['TextColor', 'BGColor'],
            # ??????
            ['Link', 'Unlink'],
            # ??????
            ['NumberedList', 'BulletedList'],
            # ?????????
            ['Maximize']
        ],
        # ?????????????????????
        'extraPlugins': ','.join(['codesnippet', 'prism', 'widget', 'lineutils']),
    }
}
