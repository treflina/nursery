from datetime import date, datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView
from django_htmx.http import trigger_client_event
from django_tables2 import SingleTableMixin

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
        if self.request.htmx and (
            self.request.headers.get("HX-Target")
            not in ["children-main", "children", "children-wrapper"]
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

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        created_obj = self.request.session.pop("created_obj", None)
        if created_obj:
            msg = _("Child has been added")
            return trigger_client_event(response, "showToast", {"msg": msg})
        return response


class ChildCreateView(CreateView):
    model = Child
    form_class = ChildForm
    template_name = "kids/child_form.html"
    success_url = reverse_lazy("kids:children")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["creating"] = True
        return context

    def get_success_url(self):
        self.request.session["created_obj"] = True
        return super().get_success_url()


class ChildUpdateView(UpdateView):
    model = Child
    form_class = ChildForm
    template_name = "kids/child_form.html"
    success_url = reverse_lazy("kids:children")

    def get_success_url(self):
        url = reverse("absences:absences_list")
        if "next" in self.request.GET:
            url = self.request.GET["next"]
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        redirect_to = self.request.GET.get("next", "")
        self.request.session["updated_obj"] = self.kwargs.get("pk")
        context["updating"] = True
        context["redirect_to"] = redirect_to
        return context


@require_http_methods(["DELETE"])
def delete_child(request, pk):
    if request.htmx:
        child_to_delete = Child.objects.filter(pk=pk).last()
        if child_to_delete:
            parent = child_to_delete.parent
            if parent and parent.child_set.count() == 1:
                parent.delete()
            child_to_delete.delete()
        resp = HttpResponse("")
        msg = _("Child has been deleted.")
        trigger_client_event(resp, "childDeleted")
        return trigger_client_event(resp, "showToast", {"msg": msg})
