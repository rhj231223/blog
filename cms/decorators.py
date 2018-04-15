# coding:utf-8
from functools import wraps
import pickle

from django.shortcuts import redirect,reverse

from cms.models import User
from configs import CMS_SEESION_ID

def login_required(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        session_id=request.session.get(CMS_SEESION_ID) if hasattr(request,'session') else None
        if session_id:

            user=User.objects.filter(username=session_id).first()
            if user:
                return func(request,*args,**kwargs)
            return redirect('{}'.format(reverse('cms_login')))
        else:
            return redirect('{}'.format(reverse('cms_login')))
    return wrapper