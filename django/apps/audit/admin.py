from functools import partial
from typing import Callable

from django.contrib.admin import ModelAdmin, register, RelatedOnlyFieldListFilter

from apps.audit.models import AuditLog


@register(AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = (
        'user',
        'get_action_display',
        'table_name',
        'action_tstamp_clk',
        'data',
        'changed',
    )

    list_filter = (
        'action',
        'table_name',
        ('user', RelatedOnlyFieldListFilter)
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.select_related('user')

    dumper: Callable[[str], Callable[['AuditLogAdmin', AuditLog], str]] = lambda attr: lambda _, obj: ', '.join(
        map(
            '='.join,
            map(
                partial(map, str),
                (getattr(obj, attr) or dict()).items()
            )
        )
    )

    data = dumper('row_data')
    changed = dumper('changed_fields')
