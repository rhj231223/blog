# coding:utf-8

from django import forms
from django.forms import Form

from utils.xtredis import BBS_Redis
from utils import xtjson

class BaseForm(Form):

    def set_request(self,request):
        self.request=request

    def get_error(self):
        key,value=self.errors.popitem()
        messages=key+':'+value[0]
        return messages

    def get_error_response(self):
        if self.errors:
            return xtjson.json_params_error(message=self.errors.as_text())


    def get_error_self_response(self):
        if self.errors:
            return xtjson.json_params_error(message=self.get_error())




class GraphCaptchaForm(BaseForm):
    captcha = forms.CharField(min_length=4, max_length=4)

    def clean(self):
        captcha = self.cleaned_data.get('captcha')
        if captcha:
            captcha = captcha.lower()
            cache_captcha = BBS_Redis.get(captcha)
            if not cache_captcha or cache_captcha.lower() != captcha:
                self.add_error('captcha', '验证码输入有误!')
            else:
                return self.cleaned_data