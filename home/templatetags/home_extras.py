from django.template import Variable, VariableDoesNotExist
from django import template

from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter
def hash(object, attr):
    pseudo_context = { 'object' : object }
    try:
        value = Variable('object.%s' % attr).resolve(pseudo_context)
    except VariableDoesNotExist:
        value = None
    return value


@register.filter
def listitem(object, i):
    return object[i]


@register.filter(name='get_class')
def get_class(value):
  return value.__class__.__name__


@register.filter(name='get_contenttype')
def get_contenttype(value):
    return ContentType.objects.get_for_model(value).id

