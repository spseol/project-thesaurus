import operator
from functools import reduce

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
        return reduce(
            operator.or_,
            map(
                lambda m: Q(**{
                    f'row_data__{str(m.key_name)}': key_value,
                    'table_name': m.model
                }),
                models
            ),
            Q(),
        )
