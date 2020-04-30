import re
from functools import cached_property

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext as _

from apps.utils.models import BaseTimestampedModel


class Thesis(BaseTimestampedModel):
    """Thesis as a single object, with all needed information."""

    class State(TextChoices):
        CREATED = 'created', _('Created')
        READY_FOR_SUBMIT = 'ready_for_submit', _('Ready for submit')
        SUBMITTED = 'submitted', _('Submitted')
        READY_FOR_REVIEW = 'ready_for_review', _('Ready for reviews')
        REVIEWED = 'reviewed', _('Reviewed')
        PUBLISHED = 'published', _('Published')

    category = models.ForeignKey(
        to='thesis.Category',
        on_delete=models.PROTECT,
        related_name='thesis_category',
        help_text=_('Corresponding category for thesis.')
    )

    authors = models.ManyToManyField(
        to=get_user_model(),
        through='thesis.ThesisAuthor',
        verbose_name=_('Authors'),
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
        null=True,
    )

    registration_number = models.CharField(
        verbose_name=_('Registration number'),
        max_length=4,
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                regex=re.compile(r'[A-Z]\d{3}'),
                message=_('Thesis registration number is not valid.')
            )
        ]
    )

    state = models.CharField(
        verbose_name=_('State'),
        max_length=32,
        choices=State.choices,
        default=State.CREATED.value
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

    reservable = models.BooleanField(
        verbose_name=_('Reservable'),
        default=True,
    )

    class Meta:
        ordering = ['registration_number']
        verbose_name = _('Thesis')
        verbose_name_plural = _('Theses')

    def __str__(self):
        return f'{self.title} ({", ".join(tuple(map(str, self.authors.all()))) or "---"})'.strip()

    @cached_property
    def available_for_reservation(self) -> bool:
        """Is this Thesis currently available for reservation?"""
        from .reservation import Reservation

        return not self.thesis_reservation.filter(
            state__in=(
                Reservation.State.READY,
                Reservation.State.RUNNING,
            )
        ).exists()

    @cached_property
    def open_reservations_count(self) -> int:
        """Returns count of reservations for this thesis in states"""
        from .reservation import Reservation

        return self.thesis_reservation.exclude(
            state__in=Reservation.State.FINISHED,
        ).count()


class ThesisAuthor(BaseTimestampedModel):
    author = models.ForeignKey(
        to=get_user_model(),
        related_name='thesis_author_author',
        on_delete=models.PROTECT
    )
    thesis = models.ForeignKey(
        to='thesis.Thesis',
        related_name='thesis_author_thesis',
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ['author', 'created']
        verbose_name = _('Thesis author relation')
        verbose_name_plural = _('Thesis author relations')
