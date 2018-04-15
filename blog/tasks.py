# coding:utf-8

from __future__ import absolute_import, unicode_literals

import time
from celery import Celery,shared_task,platforms

platforms.C_FORCE_ROOT=True

# celery=Celery('dj_project',broker='redis://:2312231223@192.168.1.4:6379/0',
#                   backend='redis://:2312231223@192.168.1.4:6379/0')



@shared_task
def add(x,y):
    time.sleep(5)