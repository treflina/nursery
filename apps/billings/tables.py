import django_tables2 as tables

from apps.core.utils.helpers import rows_higlighter

from .models import Billing


class BillingsHTMxBulkActionTable(tables.Table):

    selection = tables.CheckBoxColumn(
        accessor="pk", orderable=False, attrs={"td__input": {"@click": "checkRange"}}
    )

    zus_transfer = tables.Column(accessor="zus_transfer", orderable=False)
    paid = tables.Column(accessor="paid", orderable=False)

    class Meta:
        model = Billing
        template_name = "tables/table_htmx.html"
        show_header = False
        exclude = ("created_at", "updated_at", "changed_by")
        sequence = ("selection", "...")
        row_attrs = {"class": rows_higlighter}
        attrs = {"class": "table checkcolumn-table"}

    def __init__(self, selected_rows=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The selection parameter is a list of product ids
        # that are recently updated.
        self.selected_rows = selected_rows
        return
