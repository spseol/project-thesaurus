from django.db.models import QuerySet, Manager


class OpenReservationsManager(Manager):
    def get_queryset(self) -> 'QuerySet':
        return super().get_queryset().filter(
            state__in=self.model.OPEN_RESERVATION_STATES
        )
