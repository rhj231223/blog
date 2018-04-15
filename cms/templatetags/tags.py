# coding:utf-8
from django.template import Library
from django.template.defaultfilters import stringfilter

register=Library()

@register.filter(name='format')
@stringfilter
def format_template(value,li):
    if '{}' in value:
        value.format(*li)
        return value
    else:
        return value

