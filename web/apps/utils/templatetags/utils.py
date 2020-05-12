import json

from django import template
from django.conf import settings
from django.db.models import Choices, Model
from django.urls import reverse

register = template.Library()


@register.filter(is_safe=True)
def to_json(v):
    return json.dumps(v)


@register.simple_tag
def get_version(*_):
    return settings.VERSION


@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)


@register.filter
def get_choices_display(value, choices: Choices):
    return choices(value).label


@register.simple_tag
def get_verbose_field_name(instance: Model, field_name: str):
    return instance._meta.get_field(field_name).verbose_name


@register.simple_tag(takes_context=True)
def absolute_url(context, view_name, *args, **kwargs):
    return context['request'].build_absolute_uri(
        reverse(view_name, args=args, kwargs=kwargs)
    )
