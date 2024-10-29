from autocomplete import HTMXAutoComplete, widgets
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Parent


class ParentHTMXAutocomplete(HTMXAutoComplete):
    """Autocomplete component to select Data Sources from a library"""

    name = "username"
    model = Parent
    minimum_search_length = 2
    placeholder = _("Start typing to search")

    def get_items(self, search=None, values=None):
        data = Parent.objects.all()
        if search is not None:
            items = [
                {"label": str(x), "value": x.username}
                for x in data
                # Refactor so equality comparison is a function passed in?
                if search == "" or str(search).upper() in f"{x}".upper()
            ]
            return items
        if values is not None:
            items = [
                {"label": str(x), "value": x.username}
                for x in data
                if x.username in values
            ]
            return items

        return []


class ParentForm(forms.ModelForm):

    password2 = forms.CharField(
        label=_("Repeat password"),
        widget=forms.PasswordInput(
            attrs={
                "class": """
            border-2 border-blue-300 rounded-md
            focus:ring-[#92F398] focus:border-[#92F398] bg-white
            """
            }
        ),
    )

    class Meta:
        model = Parent
        fields = ["username", "email", "password", "password2"]
        base_class = """border-2 border-blue-300 rounded-md
                focus:ring-[#92F398] focus:border-[#92F398] bg-white"""
        widgets = {
            "username": forms.TextInput(attrs={"class": base_class}),
            "password": forms.PasswordInput(attrs={"class": base_class}),
            "email": forms.EmailInput(attrs={"class": base_class}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise ValidationError(_("Passwords don't match"))
        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ParentChangeEmailForm(forms.ModelForm):

    username = forms.CharField(
        widget=widgets.Autocomplete(
            name="username",
            use_ac=ParentHTMXAutocomplete,
            attrs={
                "component_id": "id_username",
                "id": "id_username__textinput",
                "autocomplete": "off",
            },
        )
    )

    class Meta:
        model = Parent
        fields = ["email"]
        base_class = """border-2 border-blue-300 rounded-md
                focus:ring-[#92F398] focus:border-[#92F398] bg-white"""
        widgets = {
            # "username":
            "email": forms.EmailInput(attrs={"class": base_class}),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not Parent.objects.filter(username=username).exists():
            raise ValidationError(_("Username is invalid."))
        return username


class ParentChangePasswordForm(forms.ModelForm):

    username = forms.CharField(
        widget=widgets.Autocomplete(
            name="username",
            use_ac=ParentHTMXAutocomplete,
            attrs={
                "component_id": "id_username",
                "id": "id_username__textinput",
                "autocomplete": "off",
            },
        )
    )

    password2 = forms.CharField(
        label=_("Repeat password"),
        widget=forms.PasswordInput(
            attrs={
                "class": """border-2 border-blue-300 rounded-md
                focus:ring-[#92F398] focus:border-[#92F398] bg-white"""
            }
        ),
    )

    class Meta:
        model = Parent
        fields = ["password", "password2"]
        base_class = """border-2 border-blue-300 rounded-md
                focus:ring-[#92F398] focus:border-[#92F398] bg-white"""
        widgets = {
            "password": forms.PasswordInput(attrs={"class": base_class}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise ValidationError(_("Passwords don't match"))
        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not Parent.objects.filter(username=username).exists():
            raise ValidationError(_("Username is invalid."))
        return username


class GetParentForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": """
                border-2 border-blue-300 rounded-md
                focus:ring-[#92F398] focus:border-[#92F398] bg-white
                """,
                "autocomplete": "off",
            }
        )
    )
    confirmation = forms.BooleanField(
        label=_("I'm sure I want to delete the user."),
        widget=forms.CheckboxInput(
            attrs={
                "class": """w-4 h-4 text-blue-600 bg-white border-gray-300 rounded
                        focus:ring-blue-500 dark:focus:ring-blue-600 focus:ring-2"""
            }
        ),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not Parent.objects.filter(username=username).exists():
            raise ValidationError(_("Username is invalid."))
        return username
