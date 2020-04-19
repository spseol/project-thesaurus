from django.db import models
from django.utils.translation import gettext as _

from apps.utils.models import BaseTimestampedModel


class Reservation(BaseTimestampedModel):
    """Reservation defined by thesis and user, which want to borrow the thesis."""

    thesis = models.ForeignKey(
        to='thesis.Thesis',
        related_name='thesis_reservation',
        verbose_name=_('Thesis for borrow'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')
