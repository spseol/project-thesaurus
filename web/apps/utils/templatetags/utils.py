import json

from django import template
from django.conf import settings

register = template.Library()


@register.filter(is_safe=True)
def to_json(v):
    return json.dumps(v)


@register.simple_tag
def get_version(*_):
    return settings.VERSION
