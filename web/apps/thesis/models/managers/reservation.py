from django.db.models import QuerySet, Manager


class OpenReservationsManager(Manager):
    def get_queryset(self) -> 'QuerySet':
        return super().get_queryset().exclude(
            state=self.model.State.FINISHED
        )
