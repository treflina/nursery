from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Parent


class ParentForm(forms.ModelForm):

    password2 = forms.CharField(widget= forms.PasswordInput)

    class Meta:
        model = Parent
        fields = ["username", "password", "password2", "is_active"]
        widgets = {
            "password": forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise ValidationError(_("Passwords don't match"))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
