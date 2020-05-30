import operator
import typing
from functools import reduce

from django.db.models import Manager, Model, Q, ManyToOneRel, ManyToManyField
from django.db.models.options import Options

if typing.TYPE_CHECKING:
    from apps.accounts.models import User


class AuditLogManager(Manager):
    def by_user(self, user: 'User'):
        return self.filter(
            user=user
        )

    def for_instance(self, instance: Model):
        meta: Options = instance._meta

        fields = self.get_referencing_columns(meta=meta)

        related_pk = str(instance.pk)
        return self.filter(
            reduce(
                operator.or_,
                map(
                    # {column_fk_to_instance: instance_pk} in row or in changed
                    lambda f: Q(row_data__contains={f: related_pk}) | Q(changed_fields__contains={f: related_pk}),
                    fields
                ),
            ) | Q(
                table_name=instance._meta.db_table,
                row_data__id=instance.pk,
            )
        )

    @staticmethod
    def get_referencing_columns(meta: Options):
        fk_fields_to_instance = meta.get_fields()

        # turbo magic, examples for instance = User()
        return {
            # user_id
            f'{meta.model_name}_id',
            # supervisor_id, author_id, ...
            *(rel.remote_field.column for rel in fk_fields_to_instance if isinstance(rel, ManyToOneRel)),
            # native m2m field, eg Group.users.user_id
            *(m2m_field.m2m_column_name() for m2m_field in fk_fields_to_instance if
              isinstance(m2m_field, ManyToManyField)),
        }
