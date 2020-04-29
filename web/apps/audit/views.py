# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView

from .conf import settings as audit_settings
from .forms import UsedModel
from .models import LoggedActions


class HistoryView(TemplateView):
    template_name = "audit/history_form.html"

    def get(self, request, *args, **kwargs):
        return super(HistoryView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        context['history_data'] = self.__get_history_data()
        return context

    def __get_history_data(self):
        used_models = self.kwargs.get('tables', '').split('-')
        key_name = self.kwargs.get('keyName', '').split('-')
        used_models = tuple(
            UsedModel(model=m, key_name=k)
            for m, k
            in zip(used_models, key_name)
        )

        return LoggedActions.objects.get_modifications(
            used_models,
            self.kwargs.get('keyValue'),
            audit_settings.FORM_LIMIT
        )
