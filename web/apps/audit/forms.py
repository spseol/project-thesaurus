# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from collections import namedtuple

from django.conf import settings as base_settings
from django.core.urlresolvers import reverse
from django.utils.timezone import localtime
from django.utils.translation import ugettext as _
from olc.audit.models import LoggedActions

UsedModel = namedtuple('UsedModel', 'model key_name')


class AuditFormMixin(object):
    PARAM_SEPARATOR = u"-"

    used_models = []
    _used_models_structure = []

    def get_used_models(self):
        if not self._used_models_structure:
            self._used_models_structure = self._get_used_model_structure()
        return self._used_models_structure

    def _get_used_model_structure(self):
        return tuple(UsedModel(model.get_table_name(), key_name) for model, key_name in self.used_models)

    def _get_used_model_names(self):
        return (r.model for r in self.get_used_models())

    def _get_used_model_param(self):
        return self.PARAM_SEPARATOR.join(self._get_used_model_names())

    def _get_key_name_param(self):
        return self.PARAM_SEPARATOR.join((r.key_name for r in self.get_used_models()))

    def get_last_modified(self, key_value):
        """
        :param key_value:
        :rtype: LoggedActions
        """
        return LoggedActions.objects.get_last_modification(
            self.get_used_models(),
            key_value
        ) if key_value else None

    def get_last_modified_text(self, key_value):
        obj = self.get_last_modified(key_value)
        if obj:
            datetime = localtime(obj.action_tstamp_tx) if base_settings.USE_TZ else obj.action_tstamp_tx
            return "{} ({})".format(
                obj.session_user_name,
                datetime.strftime("%d. %m. %Y %H:%M:%S"),
            )
        return ""

    def get_history_url(self, key_value):
        if not key_value:
            return ""
        return "formDialog('{}', '{}', 'lg')".format(
            _("Show history"),
            reverse("audit:history_form",
                    args=[self._get_used_model_param(),
                          self._get_key_name_param(),
                          key_value]
                    )
        )
