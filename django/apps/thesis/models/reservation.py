from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import TextChoices, Manager
from django.utils.translation import gettext_lazy as _
from django_lifecycle import AFTER_UPDATE, hook

from apps.thesis.models.managers.reservation import OpenReservationsManager
from apps.utils.models import BaseTimestampedModel


class Reservation(BaseTimestampedModel):
    """Reservation defined by thesis and user, which want to borrow the thesis."""

    class State(TextChoices):
        CREATED = 'created', _('Waiting for prepare')
        READY = 'ready', _('Ready for pickup')
        RUNNING = 'running', _('Running')
        FINISHED = 'finished', _('Finished')
        CANCELED = 'canceled', _('Canceled')

    OPEN_RESERVATION_STATES = (State.CREATED, State.READY, State.RUNNING)

    thesis = models.ForeignKey(
        to='thesis.Thesis',
        related_name='reservation_thesis',
        verbose_name=_('Thesis for borrow'),
        on_delete=models.PROTECT,
    )

    user = models.ForeignKey(
        to=get_user_model(),
        related_name='reservation_user',
        verbose_name=_('For user'),
        on_delete=models.PROTECT,
    )

    state = models.CharField(
        verbose_name=_('State'),
        choices=State.choices,
        default=State.CREATED.value,
        max_length=32,
    )

    objects = Manager()
    open_reservations = OpenReservationsManager()

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')
        ordering = ('created',)

    @hook(AFTER_UPDATE, when='state', has_changed=True)
    def on_state_change(self):
        from apps.emails.mailers import ReservationMailer
        ReservationMailer.on_state_change(reservation=self)

    def __str__(self):
        return _('Reservation {} for {}').format(
            self.thesis,
            self.user,
        )
