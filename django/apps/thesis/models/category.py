from django.db import models
from django.utils.translation import gettext_lazy as _
from positions import PositionField

from apps.utils.models import BaseModel


class Category(BaseModel):
    """Category of submitted thesis."""

    class GradeType(models.TextChoices):
        DMP = 'dmp', _('DMP (SPŠ)')
        AP = 'ap', _('AP (VOŠ)')

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=128,
    )

    order = PositionField(
        verbose_name=_('Order'),
    )

    grade_type = models.CharField(
        max_length=3,
        choices=GradeType.choices,
        default=GradeType.DMP,
        verbose_name=_('Grade type'),
    )

    class Meta:
        ordering = ['order', 'title']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title
