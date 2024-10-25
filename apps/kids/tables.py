import django_tables2 as tables
from django_tables2 import TemplateColumn

from django.utils.translation import gettext_lazy as _

from .models import Child


class ChildrenTable(tables.Table):

    admission_date = tables.DateColumn(verbose_name=_("Admission"), format="d-m-y")
    leave_date = tables.DateColumn(verbose_name=_("Leave"), format="d-m-y")
    food_price = tables.Column(
        verbose_name=_("Food"), accessor="food_price", orderable=False
    )
    local_subsidy = TemplateColumn(
        verbose_name=_("Local subsidy"),
        accessor="local_subsidy",
        template_name="kids/includes/yes_no.html",
        orderable=False,
    )
    accions = TemplateColumn(
        verbose_name=_("Accions"),
        template_name="kids/includes/child_accions_links.html",
        orderable=False,
    )

    def render_food_price(self, value):
        return value.price

    def render_last_name(self, value, record):
        return f"{value} {record.first_name}"

    class Meta:
        model = Child
        template_name = "tables/table_htmx.html"
        show_header = False
        exclude = ("id", "parent", "first_name")
        sequence = ("last_name", "...")
