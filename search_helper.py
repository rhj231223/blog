# coding:utf-8

import blog.models as bm
from cms.models import User
from mongoengine import Q


def search(search_content):


    # tags = bm.Tag.objects.filter(name__icontains=search_content).all()
    # authors = User.objects.filter(username__icontains=search_content).all()
    # articles = bm.Article.objects.filter(Q(title__icontains=search_content) | Q(content__icontains=search_content)
    #                                      | Q(author__in=authors)).all()
    #
    # # articles = [article.to_mongo() for article in articles]
    #

    s=set()
    tags = bm.Tag.objects.filter(name__icontains=search_content).all()
    for tag in tags:
        s.update(tag.articles)

    articles=bm.Article.objects.filter(is_delete=0).all()
    authors = User.objects.filter(username__icontains=search_content).all()
    articles=filter(lambda article:article.title in search_content or
                    article.content in search_content or
                    article.author in authors,articles)
    articles = list(set(articles) | s)

    return articles


