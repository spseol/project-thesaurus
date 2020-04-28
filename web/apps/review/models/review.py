from django.db import models
from django.utils.translation import gettext as _

from apps.utils.models import BaseTimestampedModel


class Review(BaseTimestampedModel):
    """Review representing thesis review by supervisor/opponent."""

    thesis = models.ForeignKey(
        to='thesis.ThesisAuthor',
        on_delete=models.PROTECT,
        related_name='review_thesis'
    )

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
