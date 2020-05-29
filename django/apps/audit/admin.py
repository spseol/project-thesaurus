from django.contrib.admin import ModelAdmin, register

from apps.audit.models import AuditLog


@register(AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = (
        '__str__',
    )
