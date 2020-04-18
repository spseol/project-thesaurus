import re

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _

from apps.utils.models import BaseTimestampedModel


class Thesis(BaseTimestampedModel):
    """Thesis as a single object, with all needed information."""

    category = models.ForeignKey(
        to='thesis.Category',
        on_delete=models.PROTECT,
    )

    registration_number = models.CharField(
        verbose_name=_('Registration number'),
        max_length=4,
        validators=[
            RegexValidator(
                regex=re.compile(r'[A-Z]\d{3}'),
                message=_('Thesis registration number is not valid.')
            )
        ]
    )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=128,
    )

    abstract = models.TextField(
        verbose_name=_('Abstract')
    )

    pdf_file = models.CharField(
        verbose_name=_('File with thesis'),
        max_length=512,
        null=True,
        # TODO: add validation, somehow implement solving real path to file
    )

    class Meta:
        ordering = ['registration_number']
        verbose_name = _('Thesis')
        verbose_name_plural = _('Theses')
