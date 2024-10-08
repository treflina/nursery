from datetime import datetime

from django import forms

from .models import Absence


class AbsenceForm(forms.ModelForm):

    date_to = forms.DateField()
    request_timestamp = forms.DateTimeField(
        initial=datetime.now, widget=forms.HiddenInput()
    )

    class Meta:
        model = Absence
        fields = ["a_date", "reason"]
