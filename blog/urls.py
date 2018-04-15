# coding:utf-8

from django.urls import path
import blog.views as blog_view

urlpatterns=[
    path('',blog_view.blog_index,name='blog_index'),
    path('test/',blog_view.blog_test,name='blog_test'),
    path('articles/<int:page>/',blog_view.blog_articles,name='blog_articles'),
    path('article_detail/<str:article_id>/',blog_view.blog_article_detail,name='blog_article_detail'),
    path('article_detail/<str:article_id>/',blog_view.blog_article_detail,name='blog_article_detail'),
    path('add_comment/',blog_view.blog_add_comment_ajax,name='blog_add_comment_ajax'),
]