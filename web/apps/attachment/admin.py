from django.contrib.admin import ModelAdmin, register

from apps.attachment.models import Attachment, TypeAttachment


@register(Attachment)
class AttachmentAdmin(ModelAdmin):
    pass


@register(TypeAttachment)
class TypeAttachmentAdmin(ModelAdmin):
    pass
