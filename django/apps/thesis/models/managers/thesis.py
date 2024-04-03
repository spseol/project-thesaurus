from django.db.models import Exists, Count, Q, OuterRef, CharField, QuerySet, Manager
from django.db.models.functions import ExtractYear, Cast


class ThesisManager(Manager):
    def published(self) -> 'QuerySet':
        return self.filter(
            state=self.model.State.PUBLISHED
        )

    @staticmethod
    def check_state_after_review_submit(thesis: 'Thesis'):
        from apps.attachment.models import TypeAttachment
        if (
                thesis.review_thesis.filter(
                    user=thesis.supervisor
                ).exists()  # has internal review
                or
                thesis.attachment_thesis.filter(
                    type_attachment__identifier=TypeAttachment.Identifier.SUPERVISOR_REVIEW
                ).exists()  # or has external
        ) and (
                thesis.review_thesis.filter(
                    user=thesis.opponent
                ).exists()
                or
                thesis.attachment_thesis.filter(
                    type_attachment__identifier=TypeAttachment.Identifier.OPPONENT_REVIEW
                ).exists()
        ):
            thesis.state = thesis.State.REVIEWED
            thesis.save(update_fields=['state'])


class ThesisApiManager(ThesisManager):
    def get_queryset(self):
        from apps.thesis.models import Reservation

        return super().get_queryset().select_related(
            'category',
            'supervisor',
            'opponent',
        ).prefetch_related(
            'authors',
            'authors__groups',
            'attachment_thesis',
            'attachment_thesis__type_attachment',
            'review_thesis',
            'review_thesis__user',
            'reservation_thesis',
        ).annotate(
            available_for_reservation=~Exists(
                queryset=Reservation.objects.filter(
                    thesis=OuterRef('pk'),
                    state__in=Reservation.OPEN_RESERVATION_STATES,
                )
            ),
            open_reservations_count=Count(
                'reservation_thesis',
                filter=Q(reservation_thesis__state__in=Reservation.OPEN_RESERVATION_STATES),
            ),
            published_at_year=Cast(ExtractYear('published_at'), CharField())
        )
