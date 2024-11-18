from django import forms
from django.utils.translation import gettext_lazy as _

from .models import (
    AdditionalDayOff,
    FoodPrice,
    GovernmentSubsidy,
    LocalSubsidy,
    MonthlyPayment,
    OtherSubsidy,
)

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


class MonthlyPaymentForm(forms.ModelForm):

    class Meta:
        model = MonthlyPayment
        fields = ("price",)
        widgets = {
            "price": forms.TextInput(
                attrs={"min": "0", "type": "number", "class": base_class}
            ),
        }


class BaseSubsidyForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={"class": base_class}))
    amount = forms.DecimalField(
        widget=forms.TextInput(
            attrs={"min": "0", "type": "number", "class": base_class}
        )
    )


class GovernmentSubsidyForm(BaseSubsidyForm):

    class Meta:
        model = GovernmentSubsidy
        fields = (
            "name",
            "amount",
        )


class LocalSubsidyForm(forms.ModelForm):

    class Meta:
        model = LocalSubsidy
        fields = ("amount",)
        widgets = {
            "amount": forms.TextInput(
                attrs={"min": "0", "type": "number", "class": base_class}
            ),
        }


class OtherSubsidyForm(BaseSubsidyForm):

    class Meta:
        model = OtherSubsidy
        fields = (
            "name",
            "amount",
        )
