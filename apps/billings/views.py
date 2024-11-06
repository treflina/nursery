import calendar
from datetime import date

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, UpdateView
from django_filters.views import FilterView
from django_htmx.http import trigger_client_event
from django_tables2 import SingleTableMixin
from django_tables2.export.views import ExportMixin

from apps.core.models import LocalSubsidy
from apps.core.utils.absent_days import get_all_absent_days
from apps.core.utils.helpers import reverse_querystring
from apps.kids.models import Child
from apps.users.decorators import get_parent_context

from .filters import BillingsFilter
from .forms import BillingForm, BillingNoteForm
from .models import Billing
from .tables import BillingsHTMxBulkActionTable


class BillingListView(ListView):

    template_name = "billings/billing_create.html"
    model = Billing

    def get_context_data(self):
        context = super().get_context_data()
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        if year is None:
            year = date.today().year

        if month is None:
            month = date.today().month

        try:
            report_date = date(year, month, 1)
        except Exception:
            return context

        context["data"] = Billing.objects.filter(date_month=report_date).order_by(
            "child"
        )
        context["year"] = year
        context["month"] = month
        return context


@require_http_methods(["POST"])
def generate_report(request):

    year = int(request.POST.get("year"))
    month = int(request.POST.get("month"))

    report_date = date(year, month, 1)

    num_days_in_month = calendar.monthrange(year, month)[1]

    children = Child.objects.filter(
        Q(admission_date__lte=date(year, month, num_days_in_month))
        & (Q(leave_date__gte=date(year, month, 1)) | Q(leave_date=None))
    )
    # TODO select_related

    local_subs = LocalSubsidy.objects.last()

    for child in children:
        absent_days = get_all_absent_days(child, year, month)
        days_to_pay_count = num_days_in_month - len(absent_days)

        food_price_day = child.food_price.price if child.food_price else 0

        food_to_pay = days_to_pay_count * food_price_day
        loc_subsidy = local_subs.amount if (local_subs and child.local_subsidy) else 0

        gov_subsidy = child.gov_subsidy.amount if child.gov_subsidy else 0
        other_sub = child.other_subsidies_sum
        other_sub_list = child.other_subsidies_list

        obj = Billing.objects.filter(date_month=report_date, child=child).last()

        if obj:
            obj.food_price = food_price_day
            obj.food_total = food_to_pay
            obj.days_count = days_to_pay_count
            obj.local_subsidy = loc_subsidy
            obj.gov_subsidy = gov_subsidy
            obj.other_subsidies = other_sub
            obj.info_subsidies = other_sub_list
            obj.changed_by = request.user
        else:
            obj = Billing(
                date_month=report_date,
                child=child,
                food_price=food_price_day,
                food_total=food_to_pay,
                days_count=days_to_pay_count,
                local_subsidy=loc_subsidy,
                gov_subsidy=gov_subsidy,
                other_subsidies=other_sub,
                info_subsidies=other_sub_list,
                note=other_sub_list,
                changed_by=request.user,
            )
        obj.save()
    return HttpResponse("", headers={"HX-Trigger": "newReport"})


@get_parent_context
def billing(request, selected_child, children, chosendate=None):

    if chosendate is None:
        chosendate = date.today()

    if not children:
        return render(
            request,
            "billings/billing.html",
            context={"nochild": True, "chosendate": chosendate},
        )

    billing_date = date(chosendate.year, chosendate.month, 1)
    billing = Billing.objects.filter(
        child__parent_id=request.user.id,
        child_id=selected_child,
        date_month=billing_date,
    ).last()

    return render(
        request,
        "billings/billing.html",
        context={"billing": billing, "chosendate": chosendate, "reportOpen": True},
    )


class BillingsReportsView(ExportMixin, SingleTableMixin, FilterView):

    table_class = BillingsHTMxBulkActionTable
    queryset = Billing.objects.all()
    filterset_class = BillingsFilter
    paginate_by = 10
    export_name = "zestawienie_oplat"
    exclude_columns = ("selection", "paid", "sub_received")

    def get_template_names(self):
        if self.request.htmx and self.request.htmx.target != "billings":
            template_name = "tables/base_table_partial.html"
        else:
            template_name = "billings/billings_list.html"
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get recently updated absence id to set focus
        updated_note = self.request.session.pop("updated_note", None)
        context["updated_note"] = updated_note
        return context

    def get_table_kwargs(self):
        # Get the list of recently updated products.
        # Pass the list to the table kwargs.
        kwargs = super().get_table_kwargs()
        selected_rows = self.request.GET.get("selection", None)
        if selected_rows:
            selected_rows = [int(_) for _ in selected_rows.split(",")]
            kwargs["selected_rows"] = selected_rows

        return kwargs


def billing_paid_update(request, pk):
    if request.method == "POST" and request.htmx:
        if request.htmx.trigger_name == "paid":
            billing = Billing.objects.filter(id=pk).last()
            if billing.paid is False:
                billing.paid = True
            else:
                billing.paid = False
            billing.save()
        page = request.POST.get("page", 1)
        page = int(page)

        # Get the sort by column
        sort_by = request.POST.get("sort", None)

        # Get the query
        query = request.POST.get("query", "")

    return HttpResponseRedirect(
        reverse_querystring(
            "billings:billings",
            query_kwargs={
                "page": page,
                "sort": sort_by,
                "query": query
            },
        )
    )


def billing_response_updateview(request):

    if request.method == "POST" and request.htmx:
        selected_billings = request.POST.getlist("selection")

        if request.htmx.trigger_name == "activate":
            Billing.objects.filter(pk__in=selected_billings).update(paid=True)

        elif request.htmx.trigger_name == "deactivate":
            Billing.objects.filter(pk__in=selected_billings).update(paid=False)

        elif request.htmx.trigger_name == "yellow_tag":
            Billing.objects.filter(pk__in=selected_billings).update(tag="yellow")

        elif request.htmx.trigger_name == "green_tag":
            Billing.objects.filter(pk__in=selected_billings).update(tag="green")

        elif request.htmx.trigger_name == "clear_tag":
            Billing.objects.filter(pk__in=selected_billings).update(tag="")

        page = request.POST.get("page", 1)
        page = int(page)
        sort_by = request.POST.get("sort", None)
        query = request.POST.get("query", "")
        selection = ",".join(selected_billings)

    return HttpResponseRedirect(
        reverse_querystring(
            "billings:billings",
            query_kwargs={
                "page": page,
                "sort": sort_by,
                "query": query,
                "selection": selection,
            },
        )
    )


class BillingUpdateView(UpdateView):
    model = Billing
    form_class = BillingForm
    template_name = "billings/billing_form.html"

    def get_success_url(self):
        url = reverse("billings:billings")
        if "next" in self.request.GET:
            url = self.request.GET["next"]
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session["updated_obj"] = self.kwargs.get("pk")
        context["updating"] = True
        redirect_to = self.request.GET.get("next", '')
        context["redirect_to"] = redirect_to
        return context


def billing_update_notes(request, pk):

    obj = Billing.objects.filter(id=pk).last()
    request.session["updated_note"] = int(pk)

    if request.method == "POST":
        form = BillingNoteForm(request.POST, instance=obj)
        if form.is_valid():
            info = form.cleaned_data["info"]
            note = form.cleaned_data["note"]
            obj.info = info
            obj.note = note
            obj.save()
            resp = HttpResponse(status=204)
            msg = _("Note has been added/changed.")
            trigger_client_event(resp, "noteUpdateCalled")
            return trigger_client_event(resp, "showToast", {"msg": msg})
    else:
        form = BillingNoteForm(instance=obj)

    return render(
        request, "billings/billing_note_form.html", {"form2": form, "update": True}
    )


@require_http_methods(["DELETE"])
def delete_billing(request, pk):
    if request.htmx:
        billing_to_delete = Billing.objects.filter(pk=pk).last()
        if billing_to_delete:
            billing_to_delete.delete()
            resp = HttpResponse("")
            msg = _("Billing has been deleted.")
            trigger_client_event(resp, "billingDeleted")
            return trigger_client_event(resp, "showToast", {"msg": msg})
        resp = HttpResponse(status=200)
        return trigger_client_event(resp, "htmx:abort")


@require_http_methods(["DELETE"])
def delete_billings(request):
    if request.htmx:
        selected_billings = request.GET.getlist("selection")
        billings_to_delete = Billing.objects.filter(pk__in=selected_billings)
        if billings_to_delete:
            billings_to_delete.delete()
            resp = HttpResponse(status=204)
            msg = _("Selected billings have been deleted.")
            trigger_client_event(resp, "billingsDeleted")
            return trigger_client_event(resp, "showToast", {"msg": msg})
        resp = HttpResponse(status=200)
        return trigger_client_event(resp, "htmx:abort")
