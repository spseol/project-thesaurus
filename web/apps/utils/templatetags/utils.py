import json

from django import template

register = template.Library()


@register.filter(is_safe=True)
def to_json(v):
    return json.dumps(v)
