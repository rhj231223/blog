import datetime

from django.db import models
from mongo_config import conn
from mongoengine import (
EmbeddedDocumentField,EmbeddedDocument,EmbeddedDocumentListField,
Document,IntField,StringField,DateTimeField,ReferenceField,ListField,
URLField)

from cms.models import User
from configs import DEFAULT_THUMBNAIL
# Create your models here.

class Article(Document):

    title=StringField(min_length=3,max_length=30)
    thumbnail=URLField(default=DEFAULT_THUMBNAIL)
    content=StringField()
    create_time=DateTimeField(default=lambda:str(datetime.datetime.now()))
    read_count=IntField(default=0)
    is_delete=IntField(default=0)

    author=ReferenceField('User')
    tags=ListField(ReferenceField('Tag'))
    comments=ListField(ReferenceField('Comment'))


class Tag(Document):
    name=StringField(min_length=1,max_length=10,unique=True)

    articles=ListField(ReferenceField('Article'))



class Comment(Document):

    content=StringField(min_length=3)
    create_time = DateTimeField(default=lambda: str(datetime.datetime.now()))

    author = StringField(min_length=2)
    article=ReferenceField('Article')
