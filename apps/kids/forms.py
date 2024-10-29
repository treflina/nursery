from autocomplete import widgets

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.users.models import Parent
from .models import Child


class ChildForm(forms.ModelForm):

    class Meta:
        model = Child
        fields = [
            "first_name",
            "last_name",
            "parent",
            "admission_date",
            "leave_date",
            "food_price",
            "local_subsidy",
        ]

        base_class = """border-2 border-blue-300 rounded-md
                focus:ring-[#92F398] focus:border-[#92F398]"""

        widgets = {
            "first_name": forms.TextInput(attrs={"class": base_class}),
            "last_name": forms.TextInput(attrs={"class": base_class}),
            "admission_date": forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date", "class": base_class}
            ),
            "leave_date": forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date", "class": base_class}
            ),
            "parent": widgets.Autocomplete(
                name="parent",
                options=dict(
                    model=Parent,
                    item_label="username",
                    minimum_search_length=0,
                    no_result_text=_("No results found"),
                ),
            ),
            "food_price": forms.Select(
                attrs={
                    "class": """border-2 border-blue-300 rounded-md w-full
                        focus:ring-[#92F398] focus:border-[#92F398]"""
                }
            ),
            "local_subsidy": forms.CheckboxInput(
                attrs={
                    "class": """w-5 h-5 text-blue-600 bg-white border-gray-300 rounded
                        focus:ring-blue-500 dark:focus:ring-blue-600 focus:ring-2"""
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        admission_date = cleaned_data.get("admission_date")
        leave_date = cleaned_data.get("leave_date")

        if admission_date and leave_date:
            if leave_date < admission_date:
                raise ValidationError(
                    _("Leave date can't be earlier than admission date.")
                )
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_classes = ("font-semibold",)
        self.fields["admission_date"].label = _("Admission")
        self.fields["leave_date"].label = _("Leave")
        self.fields["parent"].label = _("Access account")
        self.fields["food_price"].label = _("Food price")
