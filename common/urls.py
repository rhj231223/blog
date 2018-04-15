# coding:utf-8
from django.urls import path

import common.views as common_view

urlpatterns=[
    path('captcha/',common_view.common_captcha,name='common_captcha'),
    path('qiniu_token/',common_view.common_qiniu_token,name='common_qiniu_token'),
]