from django.utils.translation import gettext_lazy as _

from .base import BaseMailer
from ...thesis.models import Reservation


class ReservationMailer(BaseMailer):
    @classmethod
    def on_state_change(cls, reservation: Reservation):
        with cls._new_message() as email:
            email.to_address = cls._build_to_address((reservation.user,))

            email.subject = cls._build_subject(
                _('Reservation for thesis {} changed state to {}').format(
                    reservation.thesis.title,
                    reservation.get_state_display()
                )
            )

            email.content = cls._render_content(
                template_name='emails/reservation/state_change.html',
                thesis=reservation.thesis,
                initial_state=Reservation.State(reservation.initial_value('state')).label,
                current_state=reservation.get_state_display(),
            )

    @classmethod
    def on_created(cls, reservation: Reservation):
        with cls._new_message() as email:
            email.to_address = cls._build_to_address((reservation.user,))

            email.subject = cls._build_subject(
                _('Reservation for thesis {} has been created').format(
                    reservation.thesis.title,
                    reservation.get_state_display()
                )
            )

            email.content = cls._render_content(
                template_name='emails/reservation/created.html',
                thesis=reservation.thesis,
            )
