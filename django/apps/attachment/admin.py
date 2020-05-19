from django.contrib.admin import ModelAdmin, register
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from apps.attachment.models import Attachment, TypeAttachment


@register(Attachment)
class AttachmentAdmin(ModelAdmin):
    pass


@register(TypeAttachment)
class TypeAttachmentAdmin(ModelAdmin, DynamicArrayMixin):
    pass
