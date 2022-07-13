from typing import Optional, TYPE_CHECKING

import filetype
from django.core.exceptions import ValidationError
from django.core.files.storage import Storage, default_storage
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.db.models import Manager
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _

default_storage: Storage = default_storage

if TYPE_CHECKING:
    from apps.thesis.models import Thesis
    from apps.attachment.models import TypeAttachment


class AttachmentManager(Manager):
    def create_from_upload(
            self,
            uploaded: UploadedFile,
            thesis: 'Thesis',
            type_attachment: 'TypeAttachment',
    ):
        file_type: Optional[filetype.Type] = filetype.guess(uploaded.readline())

        if not file_type:
            raise ValidationError(_('Unknown file type for attachment {attachment}.').format(
                attachment=type_attachment.get_identifier_display(),
            ))

        if uploaded.content_type not in type_attachment.allowed_content_types:
            raise ValidationError(
                _('Content type {content} is not allowed for type attachment {attachment}.').format(
                    content=uploaded.content_type,
                    attachment=type_attachment.get_identifier_display(),
                )
            )

        if type_attachment.max_size is not None and uploaded.size > type_attachment.max_size:
            raise ValidationError(
                _('Maximal size for {attachment} is {max_size}, {real_size} given.').format(
                    attachment=type_attachment.get_identifier_display(),
                    max_size=filesizeformat(type_attachment.max_size),
                    real_size=filesizeformat(uploaded.size),
                )
            )

        attachment = self.model(
            thesis=thesis,
            type_attachment=type_attachment,
            content_type=file_type.mime,
            size=uploaded.size,
        )

        file_path = attachment.build_file_path(file_type=file_type)

        with transaction.atomic():
            default_storage.save(
                name=file_path,
                content=uploaded.file,
            )
            attachment.file_path = file_path
            attachment.save()

        return attachment
