from typing import Optional

import filetype
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage, Storage
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.db.models import Manager
from django.utils.translation import ugettext as _

default_storage: Storage = default_storage


class AttachmentManager(Manager):
    def create_from_upload(
            self,
            uploaded,
            thesis,
            type_attachment,
    ):
        """
        :type uploaded UploadedFile
        :type thesis apps.thesis.models.thesis.Thesis
        :type type_attachment apps.attachment.models.attachment.TypeAttachment

        Typing in comment to avoid circular import.
        """
        file_type: Optional[filetype.Type] = filetype.guess(uploaded.file)

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

        # TODO: max size validation

        attachment = self.model(
            thesis=thesis,
            type_attachment=type_attachment,
            content_type=file_type.mime,
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
