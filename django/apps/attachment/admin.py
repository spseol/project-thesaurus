from django.contrib.admin import ModelAdmin, register
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from apps.attachment.models import Attachment, TypeAttachment


@register(Attachment)
class AttachmentAdmin(ModelAdmin):
    list_display = ['thesis', 'type_attachment', 'file_path', 'size', 'get_download_link']
    list_filter = ['type_attachment']

    def get_download_link(self, obj: Attachment):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            reverse('api:v1:attachment-detail', args=(obj.pk,)),
            _('Download attachment')
        )

    get_download_link.short_description = _('Download attachment')


@register(TypeAttachment)
class TypeAttachmentAdmin(ModelAdmin, DynamicArrayMixin):
    list_display = ['__str__', 'allowed_content_types', 'is_public', 'max_size']
