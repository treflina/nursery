from datetime import date

import django_filters
from django.forms.widgets import Select
from django.utils.translation import gettext_lazy as _

from apps.core.filters import BaseFilter

from .models import Absence


class AbsencesFilter(BaseFilter):

    year_end_range = date.today().year + 2
    DAY_CHOICES = [(i, i) for i in range(1, 32)]
    MONTH_NAMES = [
        _("January"),
        _("February"),
        _("March"),
        _("April"),
        _("May"),
        _("June"),
        _("July"),
        _("September"),
        _("October"),
        _("November"),
        _("December"),
    ]
    # MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]
    MONTH_CHOICES = [(month[0] + 1, month[1]) for month in enumerate(MONTH_NAMES)]
    YEAR_CHOICES = [(i, i) for i in range(2024, year_end_range)]

    month = django_filters.ChoiceFilter(
        field_name="a_date",
        method="month_filter",
        choices=MONTH_CHOICES,
        widget=Select(
            attrs={
                "class": "form-control",
                "id": "id_month",
                "hx-trigger": "change",
                "hx-get": "/absences",
                "hx-indicator": ".progress",
                "hx-target": ".table-container",
                "hx-include": "[name='year'], [name='query'], [name='day']",
                "x-data": "",
                "x-on:htmx:before-request": "$dispatch('clear-pagination-and-sort')",
            }
        ),
    )
    year = django_filters.ChoiceFilter(
        field_name="a_date",
        method="year_filter",
        choices=YEAR_CHOICES,
        empty_label="----",
        widget=Select(
            attrs={
                "class": "form-control",
                "hx-trigger": "change",
                "hx-target": ".table-container",
                "hx-get": "/absences",
                "hx-indicator": ".progress",
                "hx-include": "[name='month'], [name='day'], [name='query']",
                "x-data": "",
                "x-on:htmx:before-request": "$dispatch('clear-pagination-and-sort')",  # noqa: E501
            }
        ),
    )

    day = django_filters.ChoiceFilter(
        field_name="a_date",
        method="day_filter",
        choices=DAY_CHOICES,
        label="Day",
        empty_label="--",
        widget=Select(
            attrs={
                "class": "form-control",
                "hx-trigger": "change",
                "hx-target": ".table-container",
                "hx-get": "/absences",
                "hx-indicator": ".progress",
                "hx-include": "[name='year'], [name='query'], [name='month']",
                "x-data": "",
                "x-on:htmx:before-request": "$dispatch('clear-pagination-and-sort')",  # noqa: E501
            }
        ),
    )

    class Meta:
        model = Absence
        fields = ["query", "month", "year", "day"]

    def month_filter(self, qs, name, value):
        return qs.filter(a_date__month=value)

    def year_filter(self, qs, name, value):
        return qs.filter(a_date__year=value)

    def day_filter(self, qs, name, value):
        return qs.filter(a_date__day=value)
