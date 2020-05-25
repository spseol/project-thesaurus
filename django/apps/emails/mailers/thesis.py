from django.utils.translation import gettext_lazy as _

from .base import BaseMailer
from .. import logger
from ...accounts.models import User
from ...attachment.models import Attachment
from ...review.models import Review
from ...thesis.models import Thesis
from ...utils.templatetags.utils import absolute_url


class ThesisMailer(BaseMailer):
    @classmethod
    def on_state_change(cls, thesis: Thesis):
        with cls._new_message() as email:
            email.to_address = cls._build_to_address(thesis.authors.all())

            email.subject = cls._build_subject(
                _('Thesis {} changed state to {}').format(thesis.title, thesis.get_state_display())
            )

            email.content = cls._render_content(
                template_name='emails/thesis/state_change.html',
                thesis=thesis,
                initial_state=Thesis.State(thesis.initial_value('state')).label,
                current_state=thesis.get_state_display(),
            )

    @classmethod
    def on_internal_review_added(cls, review: Review):
        thesis = review.thesis

        return cls._on_review_added(
            thesis=thesis,
            reviewer=review.user,
            url=absolute_url('api:review-pdf-detail', review.pk)
        )

    @classmethod
    def on_external_review_added(cls, attachment: Attachment):
        thesis = attachment.thesis
        type_attachment = attachment.type_attachment
        reviewer_key = type_attachment.REVIEWER_BY_IDENTIFIER.get(type_attachment.identifier)

        if not reviewer_key:
            logger.error(
                'Passed attachment %s is not a review, but %s.',
                attachment, type_attachment
            )
            return

        return cls._on_review_added(
            thesis=thesis,
            reviewer=getattr(thesis, reviewer_key),
            url=absolute_url('api:v1:attachment-detail', attachment.pk)
        )

    @classmethod
    def _on_review_added(cls, thesis: Thesis, reviewer: User, url: str):
        with cls._new_message() as email:
            email.to_address = cls._build_to_address(thesis.authors.all())

            email.subject = cls._build_subject(
                _('Thesis {} has new review from {}').format(thesis.title, reviewer.full_name)
            )

            email.html_content = cls._render_content(
                template_name='emails/thesis/review_added.html',
                thesis=thesis,
                url=url,
                reviewer=reviewer.full_name,
            )
