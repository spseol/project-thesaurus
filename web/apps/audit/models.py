from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import AuditLogManager


class AuditLog(models.Model):
    event_id = models.IntegerField(primary_key=True)
    schema_name = models.CharField(_("Schema name"), max_length=64)
    table_name = models.CharField(_("Table name"), max_length=64)
    session_user_name = models.CharField(_("Username"), max_length=64)
    action_tstamp_tx = models.DateTimeField(_("Transaction start timestamp"))
    action_tstamp_stm = models.DateTimeField(_("Statement start timestamp"))
    action_tstamp_clk = models.DateTimeField(_("Wall clock time"))
    transaction_id = models.BigIntegerField(_("Transaction ID"))
    client_query = models.TextField(_("Client query"))
    action = models.CharField(_("Action"), max_length=1)
    row_data = HStoreField(_("Row data"), null=True)
    changed_fields = HStoreField(_("Changed fields"), null=True)
    statement_only = models.BooleanField(_("Statement only"))

    objects = AuditLogManager()

    def __str__(self):
        return str(self.event_id)

    class Meta:
        db_table = "logged_actions"
        managed = False  # created by sql migration
        verbose_name = _("Audit")
        verbose_name_plural = _("Audit")
        ordering = ['event_id', ]
