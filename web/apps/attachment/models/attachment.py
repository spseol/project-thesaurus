from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext as _

from apps.utils.models import BaseTimestampedModel, BaseTypeModel


class Attachment(BaseTimestampedModel):
    """Attachment representing file stored in system. """

    thesis = models.ForeignKey(
        to='thesis.Thesis',
        related_name='thesis_attachment',
        verbose_name=_('Target thesis'),
        on_delete=models.CASCADE,
    )

    type_attachment = models.ForeignKey(
        to='attachment.TypeAttachment',
        on_delete=models.CASCADE,
        related_name='type_attachment_attachment',
        verbose_name=_('Type of attachment'),
    )

    file_path = models.CharField(
        verbose_name=_('File with thesis'),
        max_length=512,
        null=True,
        # TODO: add validation, somehow implement solving real path to file
    )

    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')


def _default_allowed_content_types():
    # has to be std function, lambda is not serializable for migrations
    return ['application/pdf']


class TypeAttachment(BaseTypeModel):
    """Type of attachment signalizing for which purpose has been attachment uploaded."""
    class Identifier(models.TextChoices):
        THESIS_TEXT = 'thesis_text', _('Thesis text')
        THESIS_ASSIGMENT = 'thesis_assigment', _('Thesis assigment')
        SUPERVISOR_REVIEW = 'supervisor_review', _('Supervisor review')
        OPPONENT_REVIEW = 'opponent_review', _('Opponent review')

    identifier = models.CharField(
        verbose_name=_('Identifier'),
        unique=True,
        max_length=128,
        choices=Identifier.choices,
    )

    allowed_content_types = ArrayField(
        base_field=models.CharField(max_length=64),
        default=_default_allowed_content_types,
        verbose_name=_('List of allowed mime/content types'),
        blank=True,
    )

    class Meta:
        verbose_name = _('Type attachment')
        verbose_name_plural = _('Types attachments')
