from django.db.models import Manager, Model


class AuditLogManager(Manager):
    def for_instance(self, instance: Model):
        return self.filter(
            table_name=instance._meta.db_table,
            row_data__id=instance.pk,
        )
