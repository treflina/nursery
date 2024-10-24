from datetime import date, datetime

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from django.views.generic import CreateView
from django.urls import reverse_lazy

from apps.billings.models import Billing
from apps.users.decorators import get_parent_context

from .filters import ChildFilter
from .models import Child
from .tables import ChildrenTable


@get_parent_context
def switch_child_profile(request, selected_child, children):

    ids = sorted([child.id for child in children])
    children_count = children.count()

    selected_child_idx = ids.index(selected_child)

    if ids.index(selected_child) == children_count - 1:
        new_selected_id = ids[0]
    else:
        new_selected_id = ids[selected_child_idx + 1]

    request.session["child"] = new_selected_id

    session_chosendate = request.session.get("chosendate")
    if session_chosendate is None:
        chosendate = date.today()
    else:
        chosendate = datetime.strptime(session_chosendate, "%Y-%m-%d").date()

    billing = Billing.objects.filter(
        date_month=date(chosendate.year, chosendate.month, 1)
    ).exists()

    return render(
        request,
        "core/base-day.html",
        {"chosendate": chosendate, "children": children, "billing": billing},
    )


class ChildrenList(SingleTableMixin, FilterView):
    table_class = ChildrenTable
    queryset = Child.objects.all().order_by("last_name")
    filterset_class = ChildFilter
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/base_table_partial.html"
        else:
            template_name = "kids/children_list.html"

        return template_name


class ChildCreateView(CreateView):
    model = Child
    fields = "__all__"
    template_name = "kids/child_create.html"
    success_url = reverse_lazy("kids:children")