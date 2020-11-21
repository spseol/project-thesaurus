from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class AppView(LoginRequiredMixin, TemplateView):
    template_name = "app.html"

    def handle_no_permission(self):
        messages.warning(self.request, _('You are not authenticated, please log in.'))
        return super().handle_no_permission()
