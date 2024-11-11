from datetime import date, timedelta

from autocomplete import widgets
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.core.utils.htmx_autocomplete import ChildHTMXAutocomplete

from .models import Absence


class BaseAbsenceForm(forms.ModelForm):

    date_to = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Absence
        fields = ["a_date", "reason"]
        widgets = {
            "reason": forms.Textarea(
                attrs={
                    "class": """my-2 border-2 border-blue-300 rounded-md w-full
                    focus:ring-[#92F398] focus:border-[#92F398]""",
                    "rows": "2",
                    "maxlength": "130",
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        a_date = cleaned_data.get("a_date")
        date_to = cleaned_data.get("date_to")

        if a_date and date_to:
            if a_date > date_to:
                raise ValidationError(_("End date cannot be earlier than start date."))

        return cleaned_data


class NurseryAbsenceForm(BaseAbsenceForm):
    first_day_paid = forms.BooleanField(
        label=_("First day paid"), required=False, initial=False
    )

    TYPE_CHOICES = (("R", _("reported")), ("NR", _("not reported")), ("O", _("other")))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["absence_type"].choices = self.TYPE_CHOICES

    class Meta:
        model = Absence
        fields = ["a_date", "reason", "child", "absence_type"]
        widgets = {
            "child": widgets.Autocomplete(
                name="child",
                use_ac=ChildHTMXAutocomplete,
                attrs={
                    "component_id": "id_child",
                    "id": "id_child__textinput",
                },
            ),
            "absence_type": forms.Select(
                attrs={
                    "class": """border-2 border-blue-300 rounded-md w-full
                    focus:ring-[#92F398] focus:border-[#92F398]"""
                }
            ),
        }


class AbsenceForm(BaseAbsenceForm):
    """Absence form with stricter validation for parents use."""

    def clean_date_to(self):
        date_to = self.cleaned_data.get("date_to")
        today = date.today()

        if date_to < today:
            raise ValidationError(_("You can't submit past end date."))
        return date_to

    def clean_a_date(self):
        a_date = self.cleaned_data.get("a_date")
        today = date.today()

        if a_date < today:
            raise ValidationError(_("You can't submit past start date."))
        return a_date

    def clean(self):
        cleaned_data = super().clean()
        a_date = cleaned_data.get("a_date")
        date_to = cleaned_data.get("date_to")

        if a_date and date_to:
            future_limit_date = date.today() + timedelta(days=180)
            if a_date > future_limit_date or date_to > future_limit_date:
                raise ValidationError(
                    _(
                        "If you plan an absence in over six month, \
inform the nursery directly."
                    )
                )

            if (date_to - a_date) > timedelta(days=28):
                raise ValidationError(
                    _(
                        "Inform the nursery directly if you plan your child's absence \
lasting longer than 4 weeks."
                    )
                )
        return cleaned_data


class UpdateAbsenceForm(forms.ModelForm):

    class Meta:
        model = Absence
        fields = ["reason", "absence_type"]
        widgets = {
            "absence_type": forms.Select(
                attrs={
                    "class": """my-2 border-2 border-blue-300 rounded-md w-full
                    focus:ring-[#92F398] focus:border-[#92F398]"""
                }
            ),
            "reason": forms.Textarea(
                attrs={
                    "class": """my-2 border-2 border-blue-300 rounded-md w-full
                    focus:ring-[#92F398] focus:border-[#92F398]""",
                    "rows": "2",
                    "maxlength": "130",
                }
            ),
        }
