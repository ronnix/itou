from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class EditUserInfoForm(forms.ModelForm):
    """
    Edit a user profile.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["birthdate"].input_formats = settings.DATE_INPUT_FORMATS
        if self.instance.is_job_seeker:
            self.fields["birthdate"].required = True
            self.fields["phone"].required = True

    class Meta:
        model = get_user_model()
        fields = ["birthdate", "phone"]
        help_texts = {
            "birthdate": _("Au format jj/mm/aaaa"),
            "phone": _("Sur 10 numéros, par exemple 0610203040"),
        }