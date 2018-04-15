# coding:utf-8

from functools import wraps

from cms.models import User
from configs import CMS_SEESION_ID


class CMSUserMiddleware(object):

    def __init__(self,get_response):
        self.get_response=get_response


    def __call__(self,request):
        s_id=request.session.get(CMS_SEESION_ID)

        if s_id:
            user=User.objects.filter(username=s_id).first()
            if user:
                setattr(request,'cms_user',user)


        response=self.get_response(request)
        return response
