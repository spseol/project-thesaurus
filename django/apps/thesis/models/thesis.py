import re
from functools import cached_property
from operator import attrgetter

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from django_lifecycle import hook, AFTER_UPDATE

from apps.thesis.models.managers import ThesisApiManager, ThesisManager, ThesisImportManager
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
        null=True, blank=True,
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
        max_length=256,
    )

    abstract = models.TextField(
        verbose_name=_('Abstract'),
        null=True, blank=True,
    )

    published_at = models.DateField(
        verbose_name=_('Publication date'),
        null=True,
    )

    submit_deadline = models.DateField(
        verbose_name=_('Submit deadline'),
        null=True, blank=True,
    )

    reservable = models.BooleanField(
        verbose_name=_('Reservable'),
        default=True,
    )

    note = JSONField(
        verbose_name=_('Additional note'),
        default=dict, null=True, blank=True,
        encoder=DjangoJSONEncoder,
    )

    objects = ThesisManager()
    api_objects = ThesisApiManager()
    import_objects = ThesisImportManager()

    class Meta:
        ordering = ['registration_number']
        verbose_name = _('Thesis')
        verbose_name_plural = _('Theses')
        permissions = (
            ('can_view_unpublished_theses', _('Can view unpublished theses')),
        )

    def __str__(self):
        return f'{self.title} ({", ".join(tuple(map(attrgetter("full_name"), self.authors.all()))) or "---"})'.strip()

    def clean(self):
        super().clean()

        if not self.registration_number and self.state == self.State.PUBLISHED:
            raise ValidationError(_('Publishing thesis without filled registration number is not allowed.'))

    @cached_property
    def available_for_reservation(self) -> bool:
        """Is this Thesis currently available for reservation?"""
        from .reservation import Reservation

        return not self.reservation_thesis.filter(
            state__in=(
                Reservation.State.READY,
                Reservation.State.RUNNING,
            )
        ).exists()

    @cached_property
    def open_reservations_count(self) -> int:
        """Returns count of reservations for this thesis in states"""
        from .reservation import Reservation

        return self.reservation_thesis.filter(
            state__in=Reservation.State.OPEN_RESERVATION_STATES,
        ).count()

    STATE_HELP_TEXTS = {
        State.CREATED: _("Thesis is created with basic information and it's waiting for state change."),
        State.READY_FOR_SUBMIT: _("Thesis is currently waiting for submit from one of authors."),
        State.SUBMITTED: _("Thesis has been submitted and it needs to be pushed to reviews."),
        State.READY_FOR_REVIEW: _("Thesis is waiting for reviews from supervisor and opponent - also possible to add "
                                  "external review."),
        State.REVIEWED: _("Thesis has both reviews and it's waiting for publication."),
        State.PUBLISHED: _("Thesis is public and it's possible to borrow it."),
    }

    @hook(AFTER_UPDATE, when='state', has_changed=True)
    def on_state_change(self):
        from apps.emails.mailers import ThesisMailer
        ThesisMailer.on_state_change(thesis=self)

    _skipped_for_hooks = {'available_for_reservation', 'open_reservations_count'}


class ThesisAuthor(BaseTimestampedModel):
    author = models.ForeignKey(
        to=get_user_model(),
        related_name='thesis_author_author',
        on_delete=models.PROTECT,
    )
    thesis = models.ForeignKey(
        to='thesis.Thesis',
        related_name='thesis_author_thesis',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['author', 'created']
        verbose_name = _('Thesis author relation')
        verbose_name_plural = _('Thesis author relations')

    def __str__(self):
        return f'{self.thesis.title} <=> {self.author}'
