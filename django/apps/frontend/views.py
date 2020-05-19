from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AppView(LoginRequiredMixin, TemplateView):
    template_name = "app/app.html"
