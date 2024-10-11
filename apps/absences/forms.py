from datetime import date, timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Absence


class BaseAbsenceForm(forms.ModelForm):

    date_to = forms.DateField()

    class Meta:
        model = Absence
        fields = ["a_date", "reason"]

    def clean(self):
        cleaned_data = super().clean()
        a_date = cleaned_data.get("a_date")
        date_to = cleaned_data.get("date_to")

        if a_date and date_to:
            if a_date > date_to:
                raise ValidationError(_("End date cannot be earlier than start date."))

        return cleaned_data


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
