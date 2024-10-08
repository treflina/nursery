from datetime import date, timedelta

from django.urls import reverse_lazy
from django.utils.http import urlencode


def rows_higlighter(**kwargs):
    """Add highlight class to rows when the product is recently
    updated. Recently updated rows are in the table selection
    parameter."""

    selected_rows = kwargs["table"].selected_rows
    if selected_rows and kwargs["record"].pk in selected_rows:
        return "highlight-me"
    return ""


def reverse_querystring(
    view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None
):
    """Custom reverse to handle query strings.
    Usage:
        reverse(
        'app.views.my_view',
        kwargs={'pk': 123}, query_kwargs={'search': 'Bob'}
        )
    """
    base_url = reverse_lazy(
        view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app
    )
    if query_kwargs:
        return "{}?{}".format(base_url, urlencode(query_kwargs))
    return base_url


def get_next_prev_month(year, month):
    previous_year = year
    previous_month = month - 1
    if previous_month == 0:
        previous_year = year - 1
        previous_month = 12
    next_year = year
    next_month = month + 1
    if next_month == 13:
        next_year = year + 1
        next_month = 1
    calendar_months = {
        "previous_year": previous_year,
        "next_year": next_year,
        "previous_month": previous_month,
        "next_month": next_month,
    }
    return calendar_months


def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days + 1):
        yield start_date + timedelta(n)
