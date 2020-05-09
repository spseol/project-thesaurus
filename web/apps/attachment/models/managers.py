from typing import Optional

import filetype
from django.core.files.storage import default_storage, Storage
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.db.models import Manager

default_storage: Storage = default_storage


class AttachmentManager(Manager):
    def create_from_upload(
            self,
            uploaded: 'UploadedFile',
            thesis,
            type_attachment,
    ):
        file_type: Optional[filetype.Type] = filetype.guess(uploaded.file)

        if not file_type:
            raise ValueError()

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
