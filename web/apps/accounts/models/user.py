import re

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _

from apps.utils.models import BaseTimestampedModel


class User(AbstractUser):
    """Replacement for default Django user with some additional stuff."""

    # TODO: custom fields?

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
