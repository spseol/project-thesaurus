from typing import Type

from django.db.migrations.operations.base import Operation
from django.db.models import Model


class AddAuditOperation(Operation):
    reduces_to_sql = True
    reversible = True
    enabled = True

    def __init__(self, model_name, audit_rows=True, audit_text=False, excluded=('created', 'modified')):
        self._model_name = model_name
        self._audit_text = audit_text
        self._audit_rows = audit_rows
        self._excluded = excluded

    def state_forwards(self, app_label, state):
        pass  # no visible changes for Django schema

    def database_forwards(
            self, app_label, schema_editor, from_state, to_state,
    ):
        model: Type[Model] = to_state.apps.get_model(app_label, self._model_name)
        table = model._meta.db_table
        with schema_editor.connection.cursor() as cursor:
            cursor.execute('SELECT to_regclass(\'audit.logged_actions\')')
            has_audit = cursor.fetchone()[0]

        BOOLEANS = ("BOOLEAN 'f'", "BOOLEAN 't'")
        if has_audit:
            schema_editor.execute(
                'SELECT audit.audit_table({})'.format(
                    ', '.join((  # join parameters
                        f"'public.{table}'",
                        BOOLEANS[self._audit_rows],
                        BOOLEANS[self._audit_text],
                        "'{{ {} }}'".format(
                            ','.join(map(  # join as postgres array
                                lambda col: f'"{col}"',
                                map(  # extract column names from field names
                                    lambda f: model._meta.get_field(f).get_attname_column()[1],
                                    self._excluded,
                                )
                            ))
                        )
                    ))
                ),
            )

    def database_backwards(
            self, app_label, schema_editor, from_state, to_state,
    ):
        model = to_state.apps.get_model(app_label, self._model_name)
        table = model._meta.db_table
        schema_editor.execute(
            'DROP TRIGGER IF EXISTS audit_trigger_row ON {}'.format(table),
        )
        schema_editor.execute(
            'DROP TRIGGER IF EXISTS audit_trigger_stm ON {}'.format(table),
        )

    def describe(self):
        return 'Add audit triggers on model {}'.format(self._model_name)


class RemoveAuditOperation(AddAuditOperation):
    enabled = False

    def database_forwards(
            self, app_label, schema_editor, from_state, to_state,
    ):
        super().database_backwards(
            app_label, schema_editor, from_state, to_state,
        )

    def database_backwards(
            self, app_label, schema_editor, from_state, to_state,
    ):
        super().database_forwards(
            app_label, schema_editor, from_state, to_state,
        )

    def describe(self):
        return 'Remove audit triggers on model {}'.format(self._model_name)
