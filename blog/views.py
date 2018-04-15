from django.shortcuts import render,HttpResponse
from django.views.decorators.http import require_http_methods
from mongoengine import Q

from blog.tasks import add
import blog.models as bm
import configs as cfg
import blog.forms as bf
from utils.pagination import pagination
from utils import xtjson
from search_helper import search
# Create your views here.

def blog_index(request):
    return blog_articles(request,1)

def blog_test(request):

    comments=bm.Article.comments
    context=dict(comments=comments)
    return render(request,'blog_test.html',context=context)

def blog_articles(request,page):
    search_content = request.GET.get('search')
    if search_content:
        articles = search(search_content)
    else:
        articles = bm.Article.objects.filter(is_delete=0).order_by('-create_time').all()
    articles_len=len(articles) if articles else 0

    total_page,start,end,page_li,show_end_num=pagination(page,articles_len,cfg.FRONT_SINGLE_PAGE_NUM,cfg.SHOW_PAGE_NUM)
    context = dict(articles=articles[start:end],total_page=total_page,
                   page_li=page_li,show_end_num=show_end_num,
                   current_page=page,single_page_num=cfg.FRONT_SINGLE_PAGE_NUM,
                   show_page_num=cfg.FRONT_SHOW_PAGE_NUM)
    return render(request, 'blog_articles.html', context=context)

def blog_article_detail(request,article_id):

    article=bm.Article.objects.filter(id=article_id).first()
    article.read_count+=1
    article.save()
    articles=bm.Article.objects.filter(is_delete=0,id__ne=article_id).order_by('-create_time').all()[:3]
    comments=bm.Comment.objects.filter(article=article).order_by('-create_time').all()
    context=dict(article=article,articles=articles,comments=comments)
    return render(request,'blog_article_detail.html',context=context)

@require_http_methods(['POST'])
def blog_add_comment_ajax(request):
    form=bf.BlogAddCommentForm(request.POST)
    if not form.is_valid():
        return xtjson.json_params_error(message=form.get_error())
    else:
        username=form.cleaned_data.get('username')
        content=form.cleaned_data.get('content')
        article_id=form.cleaned_data.get('article_id')
        article=bm.Article.objects.filter(id=article_id).first()
        comment=bm.Comment(author=username,content=content)
        comment.article=article
        comment.save()
        article.comments.append(comment)
        article.save()
        return xtjson.json_result(message='评论添加成功!')

