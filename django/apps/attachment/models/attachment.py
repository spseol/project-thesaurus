from operator import itemgetter

from django.db import models
from django.template.defaultfilters import filesizeformat
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_better_admin_arrayfield.models.fields import ArrayField
from django_lifecycle import hook, AFTER_CREATE
from filetype import Type as FileType, get_type
from filetype.types.archive import Pdf, Zip, Rar, Tar, Gz
from filetype.types.image import Png

from apps.attachment.models.managers import AttachmentManager, default_storage
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

    size = models.IntegerField(
        verbose_name=_('Size of attachment'),
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
    def file(self):
        if not self.file_path:
            raise RuntimeError('Accessing attachment file without saving it.')
        return default_storage.open(self.file_path)

    @property
    def public_file_name(self):
        file_type = get_type(mime=self.content_type)
        return f'{self.thesis.registration_number or slugify(self.thesis.title)}-' \
               f'{slugify(self.type_attachment.identifier)}.{file_type.extension}'

    def __str__(self):
        return f'{self.type_attachment.get_identifier_display()} ({self.thesis})'

    @property
    def size_label(self):
        return filesizeformat(self.size)

    @hook(AFTER_CREATE)
    def check_thesis_state(self):
        from apps.thesis.models import Thesis

        Thesis.objects.check_state_after_review_submit(thesis=self.thesis)

    @hook(AFTER_CREATE)
    def notify_added_review(self):
        from apps.emails.mailers.thesis import ThesisMailer

        if self.type_attachment.identifier in TypeAttachment.REVIEWER_BY_IDENTIFIER:
            ThesisMailer.on_external_review_added(attachment=self)


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

    REVIEWER_BY_IDENTIFIER = dict(map(reversed, IDENTIFIER_BY_REVIEWER.items()))

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

    is_public = models.BooleanField(
        verbose_name=_('Is public'),
        default=False,
    )

    max_size = models.BigIntegerField(
        verbose_name=_('Max size in bytes'),
        default=5 * 1024 * 1024,  # 5 MB
        null=True, blank=True,
    )

    class Meta:
        verbose_name = _('Type attachment')
        verbose_name_plural = _('Types attachments')
