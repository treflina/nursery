import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from django_tables2 import TemplateColumn

from .models import Absence


class AbsencesTable(tables.Table):

    a_date = tables.DateColumn(format="d-m-y")
    created_at = tables.DateTimeColumn(verbose_name=_("Created at"), format="d-m-y H:i")
    reason = tables.Column(accessor="reason", orderable=False)
    absence_type = tables.Column(
        verbose_name=_("Type"), accessor="absence_type", orderable=False
    )
    accions = TemplateColumn(
        verbose_name=_("Accions"),
        template_name="absences/includes/absence_accions_links.html",
        orderable=False,
    )

    def render_absence_type(self, value):
        if value == "first day":
            return _("Yes (PD)")
        elif value == "not reported":
            return _("Yes (NZ)")
        elif value == "reported":
            return _("No")
        else:
            return _("No (Other)")

    def render_reason(self, value):
        if len(value) > 130:
            return f"{value[:130]}..."
        else:
            return value

    class Meta:
        model = Absence
        template_name = "tables/table_htmx.html"
        show_header = False
        exclude = ("changed_by", "id", "updated_at")
        sequence = ("a_date", "child", "...", "created_at", "accions")
