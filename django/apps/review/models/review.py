from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.validators import ArrayMaxLengthValidator, ArrayMinLengthValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _
from django_bleach.models import BleachField
from django_lifecycle import AFTER_CREATE, hook

from apps.utils.models import BaseTimestampedModel


class Review(BaseTimestampedModel):
    """Review representing thesis review by supervisor/opponent."""

    class GradesChoices(IntegerChoices):
        NOT_SUFFICIENT = 1, _('Not sufficient')
        GREAT = 2, _('Great')
        VERY_WELL = 3, _('Very well')
        EXCELLENT = 4, _('Excellent')

    class GradesDMPChoices(IntegerChoices):
        VYBORNY = 1, _('1 - výborný')
        CHVALITEBNY = 2, _('2 - chvalitebný')
        DOBRY = 3, _('3 - dobrý')
        DOSTATECNY = 4, _('4 - dostatečný')
        NEDOSTATECNY = 5, _('5 - nedostatečný')

    class GradesAPChoices(IntegerChoices):
        A = 1, 'A'
        B = 2, 'B'
        C = 3, 'C'
        D = 4, 'D'
        E = 5, 'E'
        F = 6, 'F'

    class DifficultyChoices(IntegerChoices):
        UNDER_AVERAGE = 1, _('Under average')
        AVERAGE = 2, _('Average')
        OVER_AVERAGE = 3, _('Over average')

    class DifficultyNewChoices(IntegerChoices):
        OVER_AVERAGE = 1, _('Over average')
        AVERAGE = 2, _('Average')
        UNDER_AVERAGE = 3, _('Under average')

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
            validators=[MinValueValidator(1), MaxValueValidator(6)],
            choices=GradesAPChoices.choices,
            help_text=_('As value between 1 and 6 inclusive.'),
        ),
        validators=[ArrayMinLengthValidator(5), ArrayMaxLengthValidator(6)],
        verbose_name=_('Grades'),
    )
    grade_proposal = models.PositiveSmallIntegerField(
        verbose_name=_('Proposed grade'),
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        help_text=_('As value between 1 and 6 inclusive.'),
        choices=GradesAPChoices.choices,
    )

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ('thesis', 'user')

    def __str__(self):
        return _('Review on {} from {}').format(self.thesis, self.user)

    GRADE_TYPE_CUTOFF_YEAR = 2026

    @staticmethod
    def get_grade_config(category_grade_type, published_at):
        """Return (choices_class, max_value, lower_is_better) for given category and publish date."""
        use_new = published_at and published_at.year >= Review.GRADE_TYPE_CUTOFF_YEAR
        if not use_new:
            return Review.GradesChoices, 4, False
        if category_grade_type == 'ap':
            return Review.GradesAPChoices, 6, True
        return Review.GradesDMPChoices, 5, True

    def get_grades_choices(self):
        choices_class, _, _ = self.get_grade_config(
            self.thesis.category.grade_type, self.thesis.published_at
        )
        return choices_class

    def get_difficulty_choices(self):
        use_new = self.thesis.published_at and self.thesis.published_at.year >= self.GRADE_TYPE_CUTOFF_YEAR
        if use_new:
            return self.DifficultyNewChoices
        return self.DifficultyChoices

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
