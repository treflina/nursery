import django_tables2 as tables
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_tables2 import TemplateColumn

from apps.core.utils.helpers import rows_higlighter

from .models import Billing


class CheckBoxColumnWithName(tables.CheckBoxColumn):
    @property
    def header(self):
        return self.verbose_name


def check_check(value, record):
    return record.paid


class BillingsHTMxBulkActionTable(tables.Table):

    selection = tables.CheckBoxColumn(
        accessor="pk", orderable=False, attrs={"td__input": {"@click": "checkRange"}}
    )
    date_month = tables.Column(_("Month"), accessor="date_month", orderable=False)
    paid = CheckBoxColumnWithName(
        verbose_name="Zapł.", accessor="paid", checked=check_check
    )
    days_count = tables.Column(_("L.dni"), accessor="days_count", orderable=False)
    food_price = tables.Column(
        _("Wyż. (dzień)"), accessor="food_price", orderable=False
    )
    food_total = tables.Column(_("Wyż. (suma)"), accessor="food_total", orderable=False)
    monthly_payment = tables.Column(
        "Opłata mies.", accessor="monthly_payment", orderable=False
    )
    local_subsidy = tables.Column(
        "Dopł. gminna", accessor="local_subsidy", orderable=False
    )
    gov_subsidy = tables.Column("Dopł. pańtwa", accessor="gov_subsidy", orderable=False)
    other_subsidies = tables.Column(
        "Dopł. inne", accessor="other_subsidies", orderable=False
    )
    sum = tables.Column("Razem", accessor="payments_sum", orderable=False)
    accions = TemplateColumn(
        verbose_name=_("Accions"),
        template_name="billings/billing_actions_links.html",
        orderable=False,
    )

    def render_date_month(self, value):
        return f"{value.month}-{value.year}"

    def render_paid(self, value, record):
        url = reverse_lazy("billings:paid_update", kwargs={"pk": record.id})
        if record.paid is True:
            checked = "checked"
        else:
            checked = ""
        return mark_safe(
            f'<input type="checkbox" name="paid" value={record.paid} \
                hx-post="{url}" {checked}/>'
        )

    class Meta:
        model = Billing
        template_name = "tables/table_htmx_bulkactions.html"
        show_header = False
        exclude = (
            "id",
            "created_at",
            "updated_at",
            "changed_by",
            "info",
            "info_subsidies",
            "note",
            "sub_received",
            "tag",
            "confirmed",
            "sent",
        )

        sequence = (
            "selection",
            "date_month",
            "child",
            "local_subsidy",
            "gov_subsidy",
            "other_subsidies",
            "days_count",
            "food_price",
            "food_total",
            "monthly_payment",
            "sum",
            "...",
        )
        row_attrs = {"class": rows_higlighter}
        attrs = {"class": "table checkcolumn-table", "th": {"class": "sticky top-0"}}

    def __init__(self, selected_rows=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The selection parameter is a list of product ids
        # that are recently updated.
        self.selected_rows = selected_rows
        return
