from django import forms

from .models import Billing


class BillingForm(forms.ModelForm):

    class Meta:
        model = Billing
        fields = (
            "days_count",
            "food_price",
            "food_total",
            "monthly_payment",
            "local_subsidy",
            "gov_subsidy",
            "other_subsidies",
            "info_subsidies",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = """border-2 border-blue-300 rounded-md \
            focus:ring-[#92F398] focus:border-[#92F398]"""
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": base_class})
        self.fields["local_subsidy"].label = "Dopłata gm. Turawa"
        self.fields["monthly_payment"].label = "Miesięczna opłata rodzica"
        self.fields["info_subsidies"].widget.attrs.update({"rows": "2"})


class BillingNoteForm(forms.ModelForm):

    class Meta:
        model = Billing
        fields = (
            "note",
            "info",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = """border-2 border-blue-300 rounded-md \
            focus:ring-[#92F398] focus:border-[#92F398]"""
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": base_class, "rows": "3"})
