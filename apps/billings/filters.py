from datetime import date

import django_filters
from django.forms.widgets import Select
from django.utils.translation import gettext_lazy as _

from apps.core.filters import BaseFilter

from .models import Billing


class BillingsFilter(BaseFilter):

    year_end_range = date.today().year + 2
    YEAR_CHOICES = [(i, i) for i in range(2024, year_end_range)]
    MONTH_NAMES = [
        _("January"),
        _("February"),
        _("March"),
        _("April"),
        _("May"),
        _("June"),
        _("July"),
        _("October"),
        _("September"),
        _("October"),
        _("November"),
        _("December"),
    ]
    # MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]
    MONTH_CHOICES = [(month[0], month[1]) for month in enumerate(MONTH_NAMES, start=1)]

    url = "/rachunki"

    month = django_filters.ChoiceFilter(
        field_name="date_month",
        method="month_filter",
        choices=MONTH_CHOICES,
        label=_("Month"),
        widget=Select(
            attrs={
                "class": "form-control",
                "hx-trigger": "change",
                # "hx-headers": "filterChange",
                "hx-get": f"{url}",
                "hx-indicator": ".progress",
                "hx-target": ".table-container",
                "hx-include": "[name='year'], [name='query']",
                "x-data": "",
                "x-on:htmx:before-request": "$dispatch('clear-pagination-and-sort')",
            }
        ),
    )
    year = django_filters.ChoiceFilter(
        field_name="date_month",
        method="year_filter",
        choices=YEAR_CHOICES,
        label=_("Year"),
        widget=Select(
            attrs={
                "class": "form-control",
                "hx-trigger": "change",
                # "hx-headers": "filterChange",
                "hx-target": ".table-container",
                "hx-get": f"{url}",
                "hx-indicator": ".progress",
                "hx-include": "[name='day'], [name='query'], [name='month']",
                "x-data": "",
                "x-on:htmx:before-request": "$dispatch('clear-pagination-and-sort')",  # noqa: E501
            }
        ),
    )

    class Meta:
        model = Billing
        fields = ["query", "month", "year"]

    def month_filter(self, qs, name, value):
        return qs.filter(date_month__month=value)

    def year_filter(self, qs, name, value):
        return qs.filter(date_month__year=value)
