from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
@stringfilter
def split(string, sep):
    "split a string using sep"
    return string.split(sep)

@register.filter
@stringfilter
def make_dict(string, sep):
    "string must has the form: 'a:b,c:d'"
    ret = {}
    for i in string.split(sep):
        k, v = i.split(':')
        yield (k,v)
