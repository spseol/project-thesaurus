import re

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _

from apps.utils.models import BaseTimestampedModel


class Thesis(BaseTimestampedModel):
    """Thesis as a single object, with all needed information."""

    category = models.ForeignKey(
        to='thesis.Category',
        on_delete=models.PROTECT,
        related_name='thesis_category',
        help_text=_('Corresponding category for thesis.')
    )

    # TODO: not only one :'(
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
        related_name='thesis_author',
    )

    supervisor = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_('Supervisor'),
        related_name='thesis_supervisor',
    )

    opponent = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_('Opponent'),
        related_name='thesis_opponent',
    )

    registration_number = models.CharField(
        verbose_name=_('Registration number'),
        max_length=4,
        unique=True,
        validators=[
            RegexValidator(
                regex=re.compile(r'[A-Z]\d{3}'),
                message=_('Thesis registration number is not valid.')
            )
        ]
    )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=128, default='',
    )

    abstract = models.TextField(
        verbose_name=_('Abstract'),
        null=True,
    )

    published_at = models.DateField(
        verbose_name=_('Publication date'),
        null=True,
    )

    class Meta:
        ordering = ['registration_number']
        verbose_name = _('Thesis')
        verbose_name_plural = _('Theses')

    def __str__(self):
        return f'{self.title} ({self.author if self.author_id else "---"})'.strip()
