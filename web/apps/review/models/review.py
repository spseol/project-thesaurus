from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.validators import ArrayMinLengthValidator, ArrayMaxLengthValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.models import BaseTimestampedModel


class Review(BaseTimestampedModel):
    """Review representing thesis review by supervisor/opponent."""

    thesis = models.ForeignKey(
        to='thesis.Thesis',
        on_delete=models.PROTECT,
        related_name='review_thesis'
    )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.PROTECT,
        related_name='review_user'
    )

    comment = models.TextField(
        verbose_name=_('Review comment'),
    )
    questions = models.TextField(
        verbose_name=_('Review questions'),
    )
    difficulty = models.PositiveSmallIntegerField(
        verbose_name=_('Difficulty'),
        help_text=_('As value between 1 and 3 inclusive, higher is harder.'),
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    grades = ArrayField(
        models.PositiveSmallIntegerField(
            validators=[MinValueValidator(1), MaxValueValidator(4)],
            help_text=_('As value between 1 and 4 inclusive, higher is better.'),
        ),
        validators=[ArrayMinLengthValidator(5), ArrayMaxLengthValidator(6)],
        verbose_name=_('Grades'),
    )
    grade_proposal = models.PositiveSmallIntegerField(
        verbose_name=_('Proposed grade'),
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    )

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ('thesis', 'user')
