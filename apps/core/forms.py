from django import forms
from django.utils.translation import gettext_lazy as _

from.models import AdditionalDayOff


class AdditionalDayOffForm(forms.ModelForm):

    day = forms.DateField(label=_("Enter date"), widget=forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date", "class": """border-2 border-blue-300 rounded-md
                focus:ring-[#92F398] focus:border-[#92F398]"""}
            ))

    class Meta:
        model = AdditionalDayOff
        fields = ("day",)
