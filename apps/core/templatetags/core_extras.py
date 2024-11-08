from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag
def url_date_format(year, month, num):
    string_date = f"{str(year)}-{str(month)}-{str(num)}"
    return datetime.strptime(string_date, "%Y-%m-%d")


@register.simple_tag
def first_day_month(year, month):
    string_date = f"{str(year)}-{str(month)}-01"
    return datetime.strptime(string_date, "%Y-%m-%d")
