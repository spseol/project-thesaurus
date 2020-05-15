from operator import itemgetter

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_better_admin_arrayfield.models.fields import ArrayField
from filetype import Type as FileType, get_type
from filetype.types.archive import Pdf, Zip, Rar, Tar, Gz
from filetype.types.image import Png

from apps.attachment.models.managers import AttachmentManager
from apps.utils.models import BaseTimestampedModel, BaseTypeModel


def _default_allowed_content_types():
    # has to be std function, lambda is not serializable for migrations
    return [Pdf.MIME]


def _content_type_choices():
    # has to be std function, lambda is not serializable for migrations
    return list(map(lambda t: (t.MIME, t.EXTENSION), (
        Pdf,
        Png,
        Zip,
        Rar,
        Tar,
        Gz,
    )))


class Attachment(BaseTimestampedModel):
    """Attachment representing file stored in system. """

    thesis = models.ForeignKey(
        to='thesis.Thesis',
        related_name='attachment_thesis',
        verbose_name=_('Target thesis'),
        on_delete=models.CASCADE,
    )

    type_attachment = models.ForeignKey(
        to='attachment.TypeAttachment',
        on_delete=models.CASCADE,
        related_name='attachment_type_attachment',
        verbose_name=_('Type of attachment'),
    )

    file_path = models.CharField(
        verbose_name=_('File with thesis'),
        max_length=512,
        null=True,
    )

    content_type = models.CharField(
        max_length=64,
        choices=_content_type_choices(),
    )

    objects = AttachmentManager()

    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')
        ordering = ('thesis', 'type_attachment__order')

    def build_file_path(self, file_type: FileType):
        pk = str(self.id)
        thesis_pk = str(self.thesis.pk)
        return f'attachment/{thesis_pk[:2]}/{thesis_pk}/{self.type_attachment.identifier}-{pk[:4]}.{file_type.extension}'

    @property
    def public_file_name(self):
        file_type = get_type(mime=self.content_type)
        return f'{self.thesis.registration_number or slugify(self.thesis.title)}-' \
               f'{slugify(self.type_attachment.identifier)}.{file_type.extension}'


class TypeAttachment(BaseTypeModel):
    """Type of attachment signalizing for which purpose has been attachment uploaded."""

    class Identifier(models.TextChoices):
        THESIS_TEXT = 'thesis_text', _('Thesis text')
        THESIS_ASSIGMENT = 'thesis_assigment', _('Thesis assigment')
        SUPERVISOR_REVIEW = 'supervisor_review', _('Supervisor review')
        OPPONENT_REVIEW = 'opponent_review', _('Opponent review')
        THESIS_POSTER = 'thesis_poster', _('Thesis poster')
        THESIS_ATTACHMENT = 'thesis_attachment', _('Thesis attachment')

    IDENTIFIER_BY_REVIEWER = {
        'supervisor': Identifier.SUPERVISOR_REVIEW,
        'opponent': Identifier.OPPONENT_REVIEW,
    }

    identifier = models.CharField(
        verbose_name=_('Identifier'),
        unique=True,
        max_length=128,
        choices=Identifier.choices,
    )

    allowed_content_types = ArrayField(
        base_field=models.CharField(
            max_length=64,
            choices=_content_type_choices(),
        ),
        default=_default_allowed_content_types,
        verbose_name=_('List of allowed mime/content types'),
        help_text=_('Available options: {}').format(
            ', '.join(tuple(map(itemgetter(0), _content_type_choices())))
        ),
        blank=True,
    )

    class Meta:
        verbose_name = _('Type attachment')
        verbose_name_plural = _('Types attachments')
