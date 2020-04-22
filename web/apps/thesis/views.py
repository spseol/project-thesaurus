from django.views.generic import CreateView

from apps.thesis.forms import ThesisCreateForm
from apps.thesis.models import Thesis


class ThesisCreateView(CreateView):
    model = Thesis
    form_class = ThesisCreateForm
