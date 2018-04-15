# coding:utf-8
from django.http import JsonResponse

from functools import wraps
import json


class HttpCode(object):
    ok=200
    params_error=400
    unpath_error=401
    method_error=405
    server_error=500

def json_decorator(method_func):
    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return method_func(result)
        return wrapper
    return outer


# 不写死 如果是flask 参数就可以改成jsonify
@json_decorator(JsonResponse)
def json_result(code=HttpCode.ok,message='',data={},kwargs={}):
    dic=dict(code=code,message=message,data=data)

    if kwargs.keys():
        dic=dict(dic,**kwargs)

    return dic

def code_decorator(func):
    @wraps(func)
    def wrapper(message):
        # 根据函数的名字的进行切片,
        # 函数名的后面要和HttpCode的一个类属性相同
        # 例如:json_params_error  HttpCode.params_error
        name=func.__name__.split('_',1)[1]
        code=getattr(HttpCode,name)
        result=json_result(code=code,message=message)
        return result
    return wrapper

@code_decorator
def json_params_error(message=''):
    pass

@code_decorator
def json_unpath_error(message=''):
    pass

@code_decorator
def json_method_error(message=''):
    pass

@code_decorator
def json_server_error(message=''):
    pass

# def json_params_error(message=''):
#     '''
#
#         参数错误
#     '''
#     return json_result(code=HttpCode.params_error,message=message)
#
#
# def json_unpath_error(message=''):
#     '''
#
#         权限错误
#     '''
#     return json_result(code=HttpCode.unpath_error, message=message)
#
#
# def json_method_error(message=''):
#     '''
#
#         方法错误
#     '''
#     return json_result(code=HttpCode.method_error, message=message)
#
#
# def json_server_error(message=''):
#     '''
#
#     服务器内部错误
#     '''
#     return json_result(code=HttpCode.server_error, message=message)

