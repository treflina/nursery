from django import forms
from django.utils.translation import gettext_lazy as _

from .models import AdditionalDayOff, FoodPrice

base_class = """border-2 border-blue-300 rounded-md
                focus:ring-[#92F398] focus:border-[#92F398]"""


class AdditionalDayOffForm(forms.ModelForm):

    day = forms.DateField(
        label=_("Enter date"),
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": base_class}
        ),
    )

    class Meta:
        model = AdditionalDayOff
        fields = ("day",)


class FoodPriceForm(forms.ModelForm):

    class Meta:
        model = FoodPrice
        fields = ("name", "price")
        widgets = {
            "name": forms.TextInput(attrs={"class": base_class}),
            "price": forms.TextInput(
                attrs={"min": "0", "type": "number", "class": base_class}
            ),
        }
