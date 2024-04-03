from django.db.models import QuerySet, Manager


class OpenReservationsManager(Manager):
    def get_queryset(self) -> 'QuerySet':
        return super().get_queryset().filter(
            state__in=self.model.State.OPEN_RESERVATION_STATES
        )
