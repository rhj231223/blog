import json
import random

from django.shortcuts import render,HttpResponse,reverse,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from mongoengine import Q
# Create your views here.

from cms.models import User
import blog.models as bm
import cms.forms as cf
from cms.decorators import login_required
from utils.hash_helper import Hash_Pwd
from utils import xtjson
from utils.pagination import pagination
from configs import CMS_SEESION_ID,SINGLE_PAGE_NUM,SHOW_PAGE_NUM,DEFAULT_THUMBNAIL
from utils.xtmail import send_mail
from search_helper import search


@login_required
def cms_index(request):
    return render(request,'cms_index.html')

def cms_create_user(request):
    username='rhj231223'
    password='2312231223'
    email='rhj231224@gmail.com'

    p=Hash_Pwd()
    pwd=p.hash_pwd(password)

    user=User(username=username,password=pwd,email=email)
    user.save()
    return HttpResponse('success')

def cms_test(request):

    # names=['Python','Django','Flask','Javascript','Reactjs','新闻','教程']
    # for i in range(100):
    #     title='标题%s' %i
    #     content='内容%s' %i
    #
    #     python_tag=bm.Tag.objects.filter(name='Python').first()
    #
    #     author=User.objects.first()
    #     article=bm.Article(title=title,content=content)
    #     article.tags.append(python_tag)
    #     article.author=author
    #     article.save()
    #
    #     python_tag.articles.append(article)
    #     python_tag.save()
    #     author.articles.append(article)
    #     author.save()
    # article=bm.Article.objects.filter(title='324234').first()



    return HttpResponse('success')


def cms_login(request):

    if request.method=='GET':
        return render(request,'cms_login.html')
    elif request.method=='POST':
        form = cf.LoginForm(request.POST)
        if not form.is_valid():
            message=form.get_error()
            context = dict(message=message)
            return render(request,'cms_login.html',context=context)
        else:
            remember=form.cleaned_data.get('remember')
            username = form.cleaned_data.get('username')
            user = User.objects.filter(username=username).first()
            request.session[CMS_SEESION_ID] = user.username
            if not remember:
                request.session.set_expiry(0)
            next=request.GET.get('next')
            if next:
                return redirect(next)

            return redirect(reverse('cms_index'))

@login_required
def cms_profile(request):
    return render(request,'cms_profile.html')


def cms_logout(request):
    request.session.pop(CMS_SEESION_ID,None)
    return redirect(reverse('cms_login'))

class ResetPwdView(View):

    @method_decorator(login_required)
    def get(self,request):
        return render(request,'cms_reset_pwd.html')

    @method_decorator(login_required)
    def post(self,request):
        form=cf.CMSResetPwdForm(request.POST)
        form.set_request(request)

        if not form.is_valid():
           return  xtjson.json_params_error(message=form.get_error())
        else:

            p=Hash_Pwd()
            pwd=p.hash_pwd(form.cleaned_data['new_pwd'])
            request.cms_user.password=pwd
            request.cms_user.save()

            return xtjson.json_result(message='密码修改成功!')

@require_http_methods(['POST'])
def cms_send_email(request):
    if request.method=='POST':
        form=cf.CMSMailForm(request.POST)
        form.set_request(request)

        if not form.is_valid():
            return xtjson.json_params_error(message=form.get_error())
        else:
            to_mail=form.cleaned_data.get('email')
            mail=send_mail(to_email=to_mail)

            if mail:
                return xtjson.json_result(message='邮件发送成功!')
            else:
                return xtjson.json_server_error(message='请检查邮箱后再试')



class ResetEmailView(View):

    @method_decorator(login_required)
    def get(self,request):
        return render(request,'cms_reset_email.html')

    @method_decorator(login_required)
    def post(self,request):
        form=cf.CMSResetEmail(request.POST)
        form.set_request(request)

        if not form.is_valid():
            return xtjson.json_params_error(message=form.get_error())
        else:

            email=form.cleaned_data.get('email')
            user=request.cms_user
            user.email=email
            user.save()
            return xtjson.json_result(message='邮箱修改成功!')

@login_required
def cms_user_manage(request):
    users=User.objects.order_by('create_time').all()
    context=dict(users=users)
    return render(request,'cms_user_manage.html',context=context)

@login_required
@require_http_methods(["POST"])
def cms_black(request):
    form=cf.CMSBlackForm(request.POST)
    if not form.is_valid():
        return xtjson.json_result(message=form.get_error())
    else:
        return xtjson.json_result()

@login_required
@require_http_methods(['GET','POST'])
def cms_post_manage(request,page):
    search_content = request.GET.get('search')
    if search_content:
        articles=search(search_content)

    else:
        articles=bm.Article.objects.order_by('-create_time').all()
    total_num=len(articles) if articles else 0

    total_page,start,end,page_li,show_end_num=pagination(page,total_num,SINGLE_PAGE_NUM,SHOW_PAGE_NUM)
    context=dict(articles=articles[start:end],total_page=total_page,
                 page_li=page_li,current_page=int(page),search_content=search_content,
                    show_page_num=SHOW_PAGE_NUM,show_end_num=show_end_num)


    return render(request,'cms_post_manage.html',context=context)


class CMSPublishPostView(View):

    @method_decorator(login_required)
    def get(self,request):
        tags=bm.Tag.objects.all()
        context=dict(tags=tags)
        return render(request,'cms_post_manage_pub.html',context=context)

    @method_decorator(login_required)
    def post(self,request):
        form=cf.CMSAddPostForm(request.POST)
        form.set_request(request)
        if not form.is_valid():
            return xtjson.json_params_error(message=form.get_error())
        else:
            title=form.cleaned_data.get('title')
            tags=request.POST.getlist('tags[]')
            content=form.cleaned_data.get('content')
            thumbnail=form.cleaned_data.get('thumbnail')
            data=dict(title=title,content=content)

            if thumbnail:
                data.update(thumbnail=thumbnail)
            else:
                content='<p><img src="{}" alt=""></p>{}'.format(DEFAULT_THUMBNAIL,content)
                data['content']=content

            article=bm.Article(**data)
            user=request.cms_user
            article.author=user
            for tag_id in tags:
                tag=bm.Tag.objects.filter(id=tag_id).first()
                if tag:
                    article.tags.append(tag)
                    article.save()
                    tag.articles.append(article)
                    tag.save()
            user.articles.append(article)
            user.save()
            return xtjson.json_result(message='帖子发布成功')

@login_required
@require_http_methods(['POST'])
def cms_add_tag(request):
    form = cf.CMSAddTagForm(request.POST,request)
    if not form.is_valid():
        return xtjson.json_params_error(message=form.get_error())
    else:
        name=form.cleaned_data.get('name')
        tag=bm.Tag(name=name)
        tag.save()

        return xtjson.json_result(message=u'标签添加成功!')


class CMSEditPostView(View):

    @method_decorator(login_required)
    def get(self,request,article_id):
        article=bm.Article.objects.filter(id=article_id).first()
        tags=bm.Tag.objects.all()
        context=dict(tags=tags,article=article)
        return render(request,'cms_post_manage_edit.html',context=context)

    @method_decorator(login_required)
    def post(self,request,article_id):
        article = bm.Article.objects.filter(id=article_id).first()
        if article:
            form=cf.CMSEditPostForm(request.POST)
            form.set_request(request)
            if not form.is_valid():
                return xtjson.json_params_error(message=form.get_error())
            else:
                title=form.cleaned_data.get('title')
                tags=request.POST.getlist('tags[]')
                content=form.cleaned_data.get('content')
                thumbnail=form.cleaned_data.get('thumbnail')

                article.title=title
                article.tags=tags
                article.content=content

                if thumbnail:
                    article.thumbnail=thumbnail

                user=request.cms_user
                article.author=user
                article.tags=[]
                tag_li=bm.Tag.objects.all()
                for tag in tag_li:
                    if article in tag.articles:
                        tag.articles.remove(article)
                        tag.save()


                for tag_id in tags:
                    tag=bm.Tag.objects.filter(id=tag_id).first()
                    if tag:
                        article.tags.append(tag)
                        tag.articles.append(article)
                        tag.save()
                article.save()
                user.articles.append(article)
                user.save()
                return xtjson.json_result(message='帖子修改成功')

@login_required
@require_http_methods(['POST'])
def cms_post_manage_delete(request,article_id):
    form=cf.CMSDeletePostForm(request.POST)
    if not form.is_valid():
        return xtjson.json_params_error(message=form.get_error())
    else:
        article_id=form.cleaned_data.get('article_id')
        to_delete=form.cleaned_data.get('to_delete')
        article=bm.Article.objects.filter(id=article_id).first()
        if article.is_delete==0:
            if to_delete==0:
                return xtjson.json_params_error(message=u'该帖子没有被删除,无需取消删除!')
            else:
                article.is_delete=1
                article.save()
                return xtjson.json_result(message=u'该帖子已被删除!')
        else:
            if to_delete==1:
                return xtjson.json_params_error(message='该帖子已被删除,无需重复操作!')
            else:
                article.is_delete = 0
                article.save()
                return xtjson.json_result(message=u'该帖子已取消删除!')