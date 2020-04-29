# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db.models import Manager, Q


class LoggedActionsManager(Manager):
    def get_last_modification(self, models, key_value):
        return self.get_queryset().filter(
            self._get_filters(
                models,
                key_value
            )
        ).order_by('-action_tstamp_tx').first()

    def get_modifications(self, models, key_value, limit=10):
        return self.get_queryset().filter(
            self._get_filters(models, key_value)
        ).order_by('-action_tstamp_tx')[:limit]

    @staticmethod
    def _get_filters(models, key_value):
        query = Q()
        for m in models:
            key = ''.join(('row_data__', str(m.key_name)))
            key_dict = {key: key_value,
                        'table_name': m.model}
            query |= Q(**key_dict)

        return query
