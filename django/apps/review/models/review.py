from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.validators import ArrayMinLengthValidator, ArrayMaxLengthValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _
from django_bleach.models import BleachField
from django_lifecycle import hook, AFTER_CREATE

from apps.utils.models import BaseTimestampedModel


class Review(BaseTimestampedModel):
    """Review representing thesis review by supervisor/opponent."""

    class GradesChoices(IntegerChoices):
        EXCELLENT = 4, _('Excellent')
        VERY_WELL = 3, _('Very well')
        GREAT = 2, _('Great')
        NOT_SUFFICIENT = 1, _('Not sufficient')

    class DifficultyChoices(IntegerChoices):
        OVER_AVERAGE = 3, _('Over average')
        AVERAGE = 2, _('Average')
        UNDER_AVERAGE = 1, _('Under average')

    thesis = models.ForeignKey(
        to='thesis.Thesis',
        on_delete=models.CASCADE,
        related_name='review_thesis'
    )
    user = models.ForeignKey(
        to='accounts.User',
        on_delete=models.PROTECT,
        related_name='review_user'
    )

    comment = BleachField(
        verbose_name=_('Review comment'),
        strip_tags=True,
    )
    questions = BleachField(
        verbose_name=_('Review questions'),
        strip_tags=True,
    )
    difficulty = models.PositiveSmallIntegerField(
        verbose_name=_('Difficulty'),
        help_text=_('As value between 1 and 3 inclusive, higher is harder.'),
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        choices=DifficultyChoices.choices,
    )
    grades = ArrayField(
        models.PositiveSmallIntegerField(
            validators=[MinValueValidator(1), MaxValueValidator(4)],
            choices=GradesChoices.choices,
            help_text=_('As value between 1 and 4 inclusive, higher is better.'),
        ),
        validators=[ArrayMinLengthValidator(5), ArrayMaxLengthValidator(6)],
        verbose_name=_('Grades'),
    )
    grade_proposal = models.PositiveSmallIntegerField(
        verbose_name=_('Proposed grade'),
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        help_text=_('As value between 1 and 4 inclusive, higher is better.'),
        choices=GradesChoices.choices,
    )

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ('thesis', 'user')

    def __str__(self):
        return _('Review on {} from {}').format(self.thesis, self.user)

    @property
    def gradings(self):
        return tuple(filter(None, (
            self.thesis.supervisor == self.user and _('Students independence during processing'),
            _('Theoretical part of the work, comprehensibility of the text'),
            _('Methods and procedures used'),
            _('Formal editing, work with sources, citations in the text'),
            _('Graphic design of the thesis'),
            _('Interpretation of conclusions, their originality and their own contribution to the work')
        )))

    @hook(AFTER_CREATE)
    def check_thesis_state(self):
        from apps.thesis.models import Thesis
        Thesis.objects.check_state_after_review_submit(thesis=self.thesis)

    @hook(AFTER_CREATE)
    def on_internal_review_added(self):
        from apps.emails.mailers.thesis import ThesisMailer
        ThesisMailer.on_internal_review_added(review=self)
