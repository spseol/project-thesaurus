from functools import cached_property

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from .managers import AuditLogManager


class AuditLog(models.Model):
    # I = insert, D = delete, U = update, T = truncate
    class ActionChoices(TextChoices):
        INSERT = 'I', _('Inserted')
        DELETE = 'D', _('Deleted')
        UPDATE = 'U', _('Updated')
        TRUNCATE = 'T', _('Truncated')

    event_id = models.IntegerField(primary_key=True, editable=False)
    schema_name = models.CharField(_("Schema name"), max_length=64)
    table_name = models.CharField(_("Table name"), max_length=64)
    user = models.ForeignKey(to=get_user_model(), verbose_name=_("Username"), null=True, on_delete=models.PROTECT,
                             db_column='user_id')
    action_tstamp_tx = models.DateTimeField(_("Transaction start timestamp"))
    action_tstamp_stm = models.DateTimeField(_("Statement start timestamp"))
    action_tstamp_clk = models.DateTimeField(_("Wall clock time"))
    transaction_id = models.BigIntegerField(_("Transaction ID"))
    client_query = models.TextField(_("Client query"))
    action = models.CharField(_("Action"), max_length=1, choices=ActionChoices.choices)
    row_data = HStoreField(_("Row data"), null=True)
    changed_fields = HStoreField(_("Changed fields"), null=True)
    statement_only = models.BooleanField(_("Statement only"))

    objects = AuditLogManager()

    def __str__(self):
        return f'Audit log: {self.user} changed {self.table_name} ({self.changed_fields})'

    class Meta:
        db_table = "logged_actions"
        managed = False  # created by sql migration
        verbose_name = _("Audit")
        verbose_name_plural = _("Audit")
        ordering = ['-action_tstamp_clk', ]

    @cached_property
    def model_name(self):
        return self.table_name.replace('_', '.')
