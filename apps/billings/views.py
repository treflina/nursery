import calendar
from datetime import date

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from apps.core.utils.absent_days import get_all_absent_days
from apps.core.utils.helpers import reverse_querystring
from apps.kids.models import Child
from apps.users.decorators import get_parent_context

from .filters import BillingsFilter
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

    for child in children:
        absent_days = get_all_absent_days(child, year, month)
        days_to_pay_count = num_days_in_month - len(absent_days)
        food_price_day = child.food_price.amount
        to_pay = days_to_pay_count * food_price_day

        obj = Billing.objects.filter(date_month=report_date, child=child).last()

        if obj:
            obj.food_price = food_price_day
            obj.food_total = to_pay
            obj.days_count = days_to_pay_count
            obj.changed_by = request.user
        else:
            obj = Billing(
                date_month=report_date,
                child=child,
                food_price=food_price_day,
                food_total=to_pay,
                days_count=days_to_pay_count,
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


class BillingsReportsView(SingleTableMixin, FilterView):

    table_class = BillingsHTMxBulkActionTable
    queryset = Billing.objects.all()
    filterset_class = BillingsFilter
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/base_table_partial.html"
        else:
            template_name = "billings/billingreports_table_bulkaction.html"

        return template_name

    def get_table_kwargs(self):
        # Get the list of recently updated products.
        # Pass the list to the table kwargs.
        kwargs = super().get_table_kwargs()
        selected_rows = self.request.GET.get("selection", None)
        if selected_rows:
            selected_rows = [int(_) for _ in selected_rows.split(",")]
            kwargs["selected_rows"] = selected_rows

        return kwargs


def billing_response_updateview(request):

    if request.method == "POST" and request.htmx:
        # Get the selected products
        selected_billings = request.POST.getlist("selection")

        # Check if the activate/deactivate button is pressed
        if request.htmx.trigger_name == "activate":

            Billing.objects.filter(pk__in=selected_billings).update(paid=True)
        elif request.htmx.trigger_name == "deactivate":

            Billing.objects.filter(pk__in=selected_billings).update(paid=False)

        # Get the page number
        page = request.POST.get("page", 1)
        page = int(page)

        # Get the sort by column
        sort_by = request.POST.get("sort", None)

        # Get the query
        query = request.POST.get("query", "")

        # Get selection
        selection = ",".join(selected_billings)

    # Redirect to table view
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
