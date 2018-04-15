# coding:utf-8
from django import forms
from django.forms import Form

from common.forms import BaseForm
import blog.models as bm

class BlogAddCommentForm(BaseForm):
    article_id=forms.CharField()
    username=forms.CharField()
    content=forms.CharField(min_length=2)

    def clean_article_id(self):
        article_id=self.cleaned_data.get('article_id')


        article=bm.Article.objects.filter(id=article_id).first()
        if not article:
            self.add_error('article_id','没有到该文章!')
        else:
            return article_id
