from io import BytesIO as StringIO

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from utils.captcha.xtcaptcha import Captcha
from utils.xtredis import BBS_Redis
from configs import ACCESS_KEY,SECRET_KEY
import qiniu

# Create your views here.

def common_captcha(request):
    text,image=Captcha.gene_code()


    out=StringIO()
    image.save(out,'png')
    out.seek(0)
    response=HttpResponse(content_type='image/png')
    response.write(out.read())

    BBS_Redis.set(text.lower(), text.lower(),ex=2*60)
    return response



def common_qiniu_token(request):
    q = qiniu.Auth(ACCESS_KEY, SECRET_KEY)
    bucket_name = 'realblog'

    token = q.upload_token(bucket_name)
    return JsonResponse(dict(uptoken=token))