from datetime import date, datetime

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy, reverse
from django.shortcuts import render

from apps.billings.models import Billing
from apps.users.decorators import get_parent_context

from .filters import ChildFilter
from .forms import ChildForm
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
        print(self.request.headers.get("HX-Target"))
        if self.request.htmx and (
            self.request.headers.get("HX-Target") != "children-main"
        ):
            template_name = "tables/base_table_partial.html"
        else:
            template_name = "kids/children_list.html"

        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get recently updated absence id to set focus
        updated_obj = self.request.session.pop("updated_obj", None)
        context["updated_obj"] = updated_obj
        return context


class ChildCreateView(CreateView):
    model = Child
    form_class = ChildForm
    template_name = "kids/child_form.html"
    success_url = reverse_lazy("kids:children")


class ChildUpdateView(UpdateView):
    model = Child
    form_class = ChildForm
    template_name = "kids/child_form.html"
    success_url = reverse_lazy("kids:children")

    def get_success_url(self):
        self.request.session["updated_obj"] = self.kwargs.get("pk")
        url = reverse("absences:absences_list")
        if "next" in self.request.GET:
            url = self.request.GET["next"]
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["updating"] = True
        return context


@require_http_methods(["DELETE"])
def delete_absence(request, pk):
    if request.htmx:
        Child.objects.filter(pk=pk).delete()
        return HttpResponse("")
