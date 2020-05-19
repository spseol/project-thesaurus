from django.db import models
from django.utils.translation import gettext_lazy as _
from positions import PositionField

from apps.utils.models import BaseModel


class Category(BaseModel):
    """Category of submitted thesis."""
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=128,
    )

    order = PositionField(
        verbose_name=_('Order'),
    )

    class Meta:
        ordering = ['order', 'title']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title
