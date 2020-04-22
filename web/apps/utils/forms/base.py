from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column
from django.forms import Form, ModelForm


class BaseFormMixin(object):
    save_and_continue_button = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False


class BaseForm(BaseFormMixin, Form):
    pass


class BaseModelForm(BaseFormMixin, ModelForm):
    def __init__(self, *args, **kwargs):
        self.updating = bool(kwargs.get('instance'))
        super().__init__(*args, **kwargs)


class Col(Column):
    css_class = 'col'


__all__ = [
    'BaseModelForm',
    'BaseForm',
    'Col',
]
