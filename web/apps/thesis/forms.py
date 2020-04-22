from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row

from apps.thesis.models import Thesis
from apps.utils.forms.base import BaseModelForm, Col


class ThesisCreateForm(BaseModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Col('title'),
                Col('category'),
            ),
            'author',
            'supervisor',
            'opponent',
        )

    class Meta:
        model = Thesis
        fields = [
            'title',
            'category',
            'author',
            'supervisor',
            'opponent',
        ]
