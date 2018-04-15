# coding:utf-8
import hashlib,time,random
from django.core import mail
from django.core.cache import cache
from django.shortcuts import redirect,reverse
from dj_project.settings import EMAIL_HOST_USER

from utils.xtredis import BBS_Redis

def send_mail(to_email,title=None,message=None):
    if not title:
        title='修改邮箱验证'


    code_li=random.sample(list(range(10)),6)
    code=''.join([str(i) for i in code_li])

    timeout=10

    BBS_Redis.set(to_email, code, ex=timeout*60)
    if not message:
        message='亲爱的用户，您的验证码为 {0} ,{1}分钟内有效'.format(code,timeout)

    try:
        mail.send_mail(subject=title,message=message,from_email=EMAIL_HOST_USER,recipient_list=[to_email],fail_silently=False)

        return True
    except Exception as e:
        return e


# def send_mail(request,email,url_name,cache_data=None,subject=None,message=None):
#     if not cache_data:
#         cache_data=email
#     code = hashlib.md5(str(time.time()) + email).hexdigest()
#     print 'code:%s' % code
#     cache.set(code, cache_data, timeout=60 * 10)
#     # 2 发送邮件到这个邮箱
#     check_url = '%s://%s' % (request.scheme, request.get_host() + reverse(url_name, kwargs=dict(code=code)))
#
#     if not subject:
#         subject=u'邮箱验证'
#     if not message:
#         message = u'您好,请点击此链接完成验证 %s \n请在10分钟内完成验证' % check_url
#
#     from_email = EMAIL_HOST_USER
#     recipient_list = [email]
#     print message
#
#     if mail.send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list):
#         return True
#     else:
#         return False


