import datetime

from django.db import models
from mongo_config import conn

from mongoengine import (
EmbeddedDocumentField,EmbeddedDocument,EmbeddedDocumentListField,
Document,IntField,StringField,DateTimeField,BooleanField,
ListField,ReferenceField,EmailField)



# Create your models here.

class User(Document):

    username=StringField(min_length=3,max_length=20,unique=True)
    password=StringField()
    create_time=DateTimeField(default=lambda :str(datetime.datetime.now()))
    is_active=IntField(default=1)
    email=EmailField()

    articles=ListField(ReferenceField('Article'))

