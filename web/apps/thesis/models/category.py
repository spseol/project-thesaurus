from django.db import models
from django.utils.translation import gettext as _

from apps.utils.models import BaseModel


class Category(BaseModel):
    """Category of submitted thesis."""
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=128,
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=_('Order')
    )

    class Meta:
        ordering = ['order', 'title']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
