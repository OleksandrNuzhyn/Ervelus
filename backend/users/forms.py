from django import forms
from .services import get_mailgun_template_list


class EmailForm(forms.Form):
    template = forms.ChoiceField(choices=get_mailgun_template_list, widget=forms.RadioSelect)