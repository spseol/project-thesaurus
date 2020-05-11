from django.db.models import Exists, Count, Q, OuterRef, CharField, QuerySet, Manager
from django.db.models.functions import ExtractYear, Cast


class ThesisManager(Manager):
    def published(self) -> 'QuerySet':
        return self.filter(
            state=self.model.State.PUBLISHED
        )


class ThesisApiManager(ThesisManager):
    def get_queryset(self):
        from apps.thesis.models import Reservation

        return super().get_queryset().select_related(
            'category',
            'supervisor',
            'opponent',
        ).prefetch_related(
            'authors',
            'attachment_thesis',
            'attachment_thesis__type_attachment',
            'review_thesis',
            'review_thesis__user',
        ).annotate(
            available_for_reservation=~Exists(
                queryset=Reservation.objects.filter(
                    thesis=OuterRef('pk'),
                    state__in=(
                        Reservation.State.CREATED,
                        Reservation.State.READY,
                        Reservation.State.RUNNING,
                    ),
                )
            ),
            open_reservations_count=Count(
                'reservation_thesis',
                filter=~Q(reservation_thesis__state=Reservation.State.FINISHED),
            ),
            published_at_year=Cast(ExtractYear('published_at'), CharField())
        )
