# coding:utf-8

from django import forms
from django.forms import Form

from common.forms import BaseForm,GraphCaptchaForm
from utils.hash_helper import Hash_Pwd
from cms.models import User
from utils.xtredis import BBS_Redis
import blog.models as bm

class LoginForm(GraphCaptchaForm):
    username=forms.CharField(min_length=3,max_length=20,required=True)
    password=forms.CharField(required=True)
    remember=forms.CharField(required=False)
    captcha = forms.CharField(min_length=4, max_length=4)



    def clean(self):

        if super(LoginForm, self).clean():
            username=self.cleaned_data.get('username')
            password=self.cleaned_data.get('password')


            user=User.objects.filter(username=username).first()

            p=Hash_Pwd()
            check_pwd=p.check_pwd(password,user.password)

            if not user or not check_pwd:
                self.add_error('password','用户名或密码错误')

            else:
                return self.cleaned_data

class CMSResetPwdForm(BaseForm):

    old_pwd=forms.CharField(required=True)
    new_pwd=forms.CharField(min_length=3,max_length=20)
    new_pwd_repeat=forms.CharField(min_length=3,max_length=20)



    def clean(self):

        old_pwd=self.cleaned_data.get('old_pwd',None)
        new_pwd=self.cleaned_data.get('new_pwd',None)
        new_pwd_repeat=self.cleaned_data.get('new_pwd_repeat',None)


        if new_pwd!=new_pwd_repeat:
            self.add_error('new_pwd','两次密码输入不一致!')

        elif old_pwd==new_pwd:
            self.add_error('new_pwd','原密码与新密码不能相同!')

        p=Hash_Pwd()

        user=self.request.cms_user

        is_real_pwd=p.check_pwd(old_pwd,user.password)

        if not is_real_pwd:
            self.add_error('old_pwd','原密码输入有误!')

        return self.cleaned_data


class CMSMailForm(BaseForm):
    email=forms.EmailField(required=True)

    def clean(self):
        email=self.cleaned_data.get('email')
        old_email = self.request.cms_user.email
        if old_email == email:
            self.add_error('email', '新旧邮箱一致无需修改!')
        else:
            return self.cleaned_data

class CMSResetEmail(CMSMailForm):
    email_captcha=forms.CharField(min_length=6,max_length=6)


    def clean(self):
        email=self.cleaned_data.get('email')
        email_captcha=self.cleaned_data.get('email_captcha')

        cache_captcha=BBS_Redis.get(email)


        if not cache_captcha or cache_captcha!=email_captcha:
            self.add_error('email_captcha','邮箱或验证码输入有误！')
        else:
            return self.cleaned_data

class CMSBlackForm(BaseForm):
    user_id=forms.CharField(required=True)
    to_active=forms.IntegerField(required=True)

    def clean(self):
        user_id=self.cleaned_data.get('user_id')
        to_active=self.cleaned_data.get('to_active')

        user=User.objects.filter(id=user_id).first()
        if not user:
            self.add_error('user_id','没有找到该用户')

        if user.is_active:
            if to_active == 1:
                self.add_error('to_active','该用户没有被封锁无需解禁！')
            else:
                user.is_active=0
                user.save()
                return self.cleaned_data
        else:
            if to_active == 0:
                self.add_error('to_active','该用户已被封锁，无需再次封锁')
            else:
                user.is_active = 1
                user.save()
                return self.cleaned_data

class CMSAddTagForm(BaseForm):
    name=forms.CharField(required=True)

    def clean_name(self):
        name=self.cleaned_data.get('name')

        old_tag=bm.Tag.objects.filter(name=name).first()

        if old_tag:
            self.add_error('name','改标签已存在')
        else:
            return name

class CMSAddPostForm(BaseForm):
    title = forms.CharField(min_length=3)
    content = forms.CharField(min_length=5)
    thumbnail=forms.URLField(required=False)

class CMSBasePostForm(BaseForm):
    article_id=forms.CharField()

    def clean_article_id(self):
        article_id=self.cleaned_data.get('article_id')
        article=bm.Article.objects.filter(id=article_id).first()

        if not article:
            self.add_error('article_id','找不到该帖子')

        else:
            return article_id


class CMSEditPostForm(CMSAddPostForm,CMSBasePostForm):
    pass


class CMSDeletePostForm(CMSBasePostForm):
    to_delete=forms.IntegerField()




