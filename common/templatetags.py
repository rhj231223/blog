# coding:utf-8
import os
from django import template

register=template.Library()

@register.simple_tag
def static_url(path):
    base_path=os.path.dirname(__file__)
    final_path=os.path.join(base_path,path)
    return final_path

