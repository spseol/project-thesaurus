from django.db.models import Manager, Exists, Count, Q, OuterRef


class ThesisApiManager(Manager):
    def get_queryset(self):
        from apps.thesis.models import Reservation

        return super().get_queryset().select_related(
            'category',
            'supervisor',
            'opponent'
        ).prefetch_related(
            'authors'
        ).annotate(
            available_for_reservation=~Exists(
                queryset=Reservation.objects.filter(
                    thesis=OuterRef('pk'),
                    state__in=(
                        Reservation.State.READY,
                        Reservation.State.RUNNING,
                    ),
                )
            ),
            open_reservations_count=Count(
                'thesis_reservation',
                filter=Q(
                    thesis_reservation__state=Reservation.State.FINISHED,
                    _negated=True,
                )
            )
        )
