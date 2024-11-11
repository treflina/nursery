from datetime import date
from autocomplete import widgets
from django import forms
from django.utils.translation import gettext_lazy as _

from apps.core.utils.htmx_autocomplete import ChildHTMXAutocomplete
from apps.core.widgets import MonthYearWidget
from apps.kids.models import Child
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


class BillingCreateForm(forms.ModelForm):

    last_billing = Billing.objects.all().order_by("date_month").last()

    date_month = forms.DateField(
        widget=MonthYearWidget(
            attrs={
                "class": """border-2 border-blue-300 rounded-md \
                focus:ring-[#92F398] focus:border-[#92F398]"""
            }
        ),
        required=True,
        label=_("Period"),
    )
    child = forms.ModelChoiceField(
        queryset=Child.objects.all(),
        required=False,
        widget=widgets.Autocomplete(
            name="child",
            use_ac=ChildHTMXAutocomplete,
            attrs={
                "component_id": "id_child",
                "id": "id_child__textinput",
            },
        ),
    )

    class Meta:
        model = Billing
        fields = ("date_month",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.last_billing.date_month.month == 12:
            m = 1
            y = self.last_billing.date_month.year + 1
        else:
            m = self.last_billing.date_month.month + 1
            y = self.last_billing.date_month.year
        self.fields["date_month"].initial = date(y, m, 1)
