# coding:utf-8

def cns_user_context_processor(request):
    if hasattr(request,'cms_user'):
        cms_user=request.cms_user
        return dict(cms_user=cms_user)
    else:
        return {}