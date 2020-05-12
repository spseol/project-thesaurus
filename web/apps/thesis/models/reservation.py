from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext as _

from apps.utils.models import BaseTimestampedModel


class Reservation(BaseTimestampedModel):
    """Reservation defined by thesis and user, which want to borrow the thesis."""

    class State(TextChoices):
        CREATED = 'created', _('Created')
        READY = 'ready', _('Ready for pickup')
        RUNNING = 'running', _('Running')
        FINISHED = 'finished', _('Finished')

    thesis = models.ForeignKey(
        to='thesis.Thesis',
        related_name='reservation_thesis',
        verbose_name=_('Thesis for borrow'),
        on_delete=models.PROTECT,
    )

    for_user = models.ForeignKey(
        to=get_user_model(),
        related_name='reservation_for_user',
        verbose_name=_('For user'),
        on_delete=models.PROTECT,
    )

    state = models.CharField(
        verbose_name=_('State'),
        choices=State.choices,
        default=State.CREATED.value,
        max_length=32,
    )

    # TODO: think about 'pre-reservations'

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')
        ordering = ('created',)

    def __str__(self):
        return _('Reservation {} for {}').format(
            self.thesis,
            self.for_user,
        )
