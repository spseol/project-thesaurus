import re
from audioop import reverse

from constance import config
from django import template
from django.conf import settings
from django.contrib.messages import get_messages
from django.db.models import Choices, Model
from django.http import HttpRequest
from django.templatetags.static import static
from django.urls import reverse
from django.utils import translation
from django.utils.html import json_script

from apps.accounts.serializers import UserSerializer

register = template.Library()


@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)


@register.filter
def get_choices_display(value, choices: Choices):
    return choices(value).label


@register.simple_tag
def get_verbose_field_name(instance: Model, field_name: str):
    return instance._meta.get_field(field_name).verbose_name


@register.simple_tag
def absolute_url(view_name, *args, **kwargs):
    return f'{settings.PUBLIC_HOST.rstrip("/")}{reverse(view_name, args=args, kwargs=kwargs)}'


@register.simple_tag(takes_context=True)
def page_context(context, element_id, _re_language=re.compile(r'[_-]'), *args, **kwargs):
    request: HttpRequest = context['request']

    user = request.user
    return json_script(dict(
        locale=_re_language.split(translation.get_language())[0],
        user=UserSerializer(instance=user).data,
        groups=tuple(user.groups.values_list('name', flat=True)),
        djangoAdminUrl=reverse('admin:index') if user.is_staff else '',
        logoutUrl=reverse('logout'),
        languages=[(k, translation.gettext(v)) for k, v in settings.LANGUAGES],
        version=settings.VERSION,

        messages=[dict(text=str(m), type=m.level_tag) for m in get_messages(request)],

        THESIS_SUBMIT_USE_CONFIRM_DIALOG=config.THESIS_SUBMIT_USE_CONFIRM_DIALOG,
    ), element_id)


@register.simple_tag
def static_absolute_local_file(path):
    # file: for local context
    # static root to bind in absolute in FS
    # standard static path resolution
    # strip static prefix (used by browsers)
    return f'file:{settings.STATIC_ROOT}/{static(path=path)[len(settings.STATIC_URL):]}'
