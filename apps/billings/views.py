import calendar
from datetime import date

from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, UpdateView
from django_filters.views import FilterView
from django_htmx.http import (
    trigger_client_event,
    HttpResponseClientRedirect,
)
from django_tables2 import SingleTableMixin
from django_tables2.export.views import ExportMixin
from xlsxwriter.workbook import Workbook

from apps.core.models import LocalSubsidy
from apps.core.utils.absent_days import get_all_absent_days
from apps.core.utils.helpers import reverse_querystring
from apps.kids.models import Child
from apps.users.decorators import get_parent_context

from .filters import BillingsFilter
from .forms import BillingForm, BillingNoteForm, BillingCreateForm
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


def generate_report(request):
    if request.method == "POST":
        form = BillingCreateForm(request.POST)

        if form.is_valid():
            date_month = form.cleaned_data["date_month"]
            child = form.cleaned_data["child"]

            year = date_month.year
            month = date_month.month
            report_date = date(year, month, 1)
            num_days_in_month = calendar.monthrange(year, month)[1]

            if child is not None:
                if (child.admission_date > date(year, month, num_days_in_month)) or (
                    child.leave_date is not None and child.leave_date < report_date
                ):
                    form.add_error(
                        "child", "Dziecko nie uczęszczało do żłobka w wybranym okresie"
                    )
                    return render(
                        request, "billings/billing_create.html", {"form2": form}
                    )
                else:
                    children = [child]
                    children_count = 1
            else:
                children = Child.objects.filter(
                    Q(admission_date__lte=date(year, month, num_days_in_month))
                    & (Q(leave_date__gte=date(year, month, 1)) | Q(leave_date=None))
                )
                children_count = children.count()
                if children_count == 0:
                    form.add_error(
                        "date_month",
                        "Brak dzieci, dla których można wygenerować \
                        rachunek w wybranym okresie.",
                    )
                    return render(
                        request, "billings/billing_create.html", {"form2": form}
                    )

            # TODO select_related
            local_subs = LocalSubsidy.objects.last()

            confirmed_count = 0

            for child in children:
                absent_days = get_all_absent_days(child, year, month)
                days_to_pay_count = num_days_in_month - len(absent_days)

                food_price_day = child.food_price.price if child.food_price else 0

                food_to_pay = days_to_pay_count * food_price_day
                loc_subsidy = (
                    local_subs.amount if (local_subs and child.local_subsidy) else 0
                )

                gov_subsidy = child.gov_subsidy.amount if child.gov_subsidy else 0
                other_sub = child.other_subsidies_sum
                other_sub_list = child.other_subsidies_list

                obj = Billing.objects.filter(date_month=report_date, child=child).last()

                if obj and obj.confirmed is True:
                    confirmed_count += 1
                elif obj and obj.confirmed is False:
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

            count = children_count - confirmed_count

            resp = HttpResponse(status=204)
            if children_count == confirmed_count and confirmed_count > 0:
                msg = _(
                    "No billings were created, because in the \
given period all are already confirmed."
                )
                trigger_client_event(resp, "showToast", {"msg": msg, "err": "true"})
            else:
                msg = _(
                    f"Billings have been successfully created. \
                    Created: {count} \nSkipped: {confirmed_count}"
                )
                trigger_client_event(resp, "showToast", {"msg": msg})

            return trigger_client_event(resp, "newReport")

    else:
        form = BillingCreateForm()
        return render(request, "billings/billing_create.html", {"form2": form})


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
    queryset = (
        Billing.objects.all()
        .order_by("-date_month", "child")
        .select_related("child__parent")
        .only("child__parent__email")
    )
    filterset_class = BillingsFilter
    paginate_by = 100
    export_name = "zestawienie_oplat"
    exclude_columns = ("selection", "paid", "sub_received", "accions")

    def get_template_names(self):
        if self.request.htmx and self.request.htmx.target not in [
            "billings",
            "billings-main",
        ]:
            template_name = "tables/billings_table_partial.html"
        else:
            template_name = "billings/billings_list.html"
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year_params = self.request.GET.get("year")
        month_params = self.request.GET.get("month")

        if year_params and month_params:
            context["export_data"] = True

        last_billing = Billing.objects.all().order_by("date_month").last()
        context["year"] = last_billing.date_month.year
        context["month"] = last_billing.date_month.month

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

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)

        if kwargs["data"] is None:
            request_dict = {}
        else:
            request_dict = kwargs["data"].dict()

        if not request_dict:
            last_billing = Billing.objects.all().order_by("date_month").last()
            request_dict.update(
                {
                    "year": last_billing.date_month.year,
                    "month": last_billing.date_month.month,
                }
            )
        kwargs["data"] = request_dict
        return kwargs


def export_xlsx_file(request, year=None, month=None):

    if not year or not month:
        last_billing = Billing.objects.all().order_by("date_month").last()
        year = last_billing.date_month.year
        month = last_billing.date_month.month
    qs = Billing.objects.filter(
        Q(date_month__month=month) & Q(date_month__year=year)
    ).order_by("child")
    if qs.count() > 100:
        qs = Billing.objects.filter(
            Q(date_month__month=month) & Q(date_month__year=year)
        ).order_by("child")[:100]

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename=zlobek_{month}_{year}"

    workbook = Workbook(response, {"in_memory": True})
    worksheet = workbook.add_worksheet("zestawienie")

    yellow = workbook.add_format({"bg_color": "#FEF9C3"})
    green = workbook.add_format({"bg_color": "#BBF7D0"})
    white = workbook.add_format({"bg_color": "white"})
    bold = workbook.add_format({"bold": True})

    row = 1
    col = 0

    for line in qs:
        if line.tag == "yellow":
            c_format = yellow
        elif line.tag == "green":
            c_format = green
        else:
            c_format = white

        worksheet.write(row, col, row, c_format)
        worksheet.write(row, col + 1, line.child.full_name, c_format)
        worksheet.write(row, col + 2, line.local_subsidy, c_format)
        worksheet.write(row, col + 3, line.gov_subsidy, c_format)
        worksheet.write(row, col + 4, line.other_subsidies, c_format)

        worksheet.write(row, col + 5, line.days_count, c_format)
        worksheet.write(row, col + 6, line.food_price, c_format)
        worksheet.write(row, col + 7, line.food_total, c_format)
        worksheet.write(row, col + 8, line.monthly_payment, c_format)
        worksheet.write(row, col + 9, line.payments_sum, c_format)
        if line.paid is True:
            worksheet.write(row, col + 10, "Tak", c_format)
        else:
            worksheet.write(row, col + 10, "Nie", c_format)
        if line.confirmed is True:
            worksheet.write(row, col + 11, "Tak", c_format)
        else:
            worksheet.write(row, col + 11, "Nie", c_format)
        worksheet.write(row, col + 12, line.info_subsidies)
        worksheet.write(row, col + 13, line.note)
        row += 1

    worksheet.write("A1", "Lp.", bold)
    worksheet.write("B1", "Dziecko", bold)
    worksheet.write("C1", "Dopł. gmina", bold)
    worksheet.write("D1", "Dopł. państwo", bold)
    worksheet.write("E1", "Dopł. inne", bold)
    worksheet.write("F1", "L.dni", bold)
    worksheet.write("G1", "Wyż.dz.", bold)
    worksheet.write("H1", "Wyż. suma", bold)
    worksheet.write("I1", "Mies.opłata", bold)
    worksheet.write("J1", "Razem", bold)
    worksheet.write("K1", "Zapłacone", bold)
    worksheet.write("L1", "Zatwierdzone", bold)
    worksheet.write("M1", "Inne dopłaty", bold)
    worksheet.write("N1", "Notatka", bold)
    worksheet.autofit()
    workbook.close()
    return response


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

        sort_by = request.POST.get("sort", None)
        query = request.POST.get("query", "")
        month = request.POST.get("month", None)
        year = request.POST.get("year", None)

    return HttpResponseRedirect(
        reverse_querystring(
            "billings:billings",
            query_kwargs={
                "page": page,
                "sort": sort_by,
                "query": query,
                "month": month,
                "year": year,
            },
        )
    )


def billing_confirm(request, pk):
    if request.method == "POST" and request.htmx:
        if request.htmx.trigger_name == "confirm":
            billing = Billing.objects.filter(id=pk).last()
            if billing:
                billing.confirmed = True
                billing.save()
                context = {"record": billing}
                return render(
                    request, "billings/includes/send_button.html", context=context
                )
    return trigger_client_event(HttpResponse(""), "htmx:abort")


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
        elif request.htmx.trigger_name == "confirm_many":
            Billing.objects.filter(pk__in=selected_billings).update(confirmed=True)

        selection = ",".join(selected_billings)

        if request.htmx.trigger_name == "delete":
            Billing.objects.filter(pk__in=selected_billings).delete()
            selection = ""

        page = request.POST.get("page", 1)
        page = int(page)
        sort_by = request.POST.get("sort", None)
        month = request.POST.get("month", None)
        year = request.POST.get("year", None)
        query = request.POST.get("query", "")

    return HttpResponseRedirect(
        reverse_querystring(
            "billings:billings",
            query_kwargs={
                "page": page,
                "sort": sort_by,
                "query": query,
                "month": month,
                "year": year,
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
        redirect_to = self.request.GET.get("next", "")
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
        if obj:
            form = BillingNoteForm(instance=obj)
        else:
            resp = HttpResponse(status=204)
            msg = _("Nie znaleziono w bazie wybranego rachunku.")
            trigger_client_event(resp, "noteUpdateCalled")
            return trigger_client_event(resp, "showToast", {"msg": msg})

    return render(
        request,
        "billings/billing_note_form.html",
        {"form2": form, "update": True, "obj": obj},
    )


def send_billing(request, pk):
    if request.method == "POST" and request.htmx:
        billing = Billing.objects.filter(id=pk).last()
        if billing.confirmed is False:
            msg = _("Before sending, confirm the billing.")
            resp = HttpResponse(status=204)
            return trigger_client_event(resp, "showToast", {"msg": msg, "err": "true"})
        if billing.child.parent is not None:
            email = billing.child.parent.email
            if email is None:
                msg = _(
                    "Email was not sent because there is no parent account assigned."
                )
            else:
                try:
                    send_mail(
                        subject=f"""Rachunek {billing.date_month.month}-
                        {billing.date_month.year}""",
                        message=f"Wyżywienie: {billing.food_total}",
                        from_email="test@example.com",
                        recipient_list=[email],
                    )
                    billing.sent = True
                    billing.save()
                    msg = _("Email has been sent.")
                    resp = HttpResponse(
                        """<p class="text-sm inline-block px-1.5
                        py-1 w-[4.7rem]">Wysłano</p>"""
                    )
                    return trigger_client_event(resp, "showToast", {"msg": msg})
                except Exception as e:
                    # TODO  handle failure
                    msg = _("Email was not sent")
                    pass
        else:
            msg = _("Email was not sent because there is no parent account assigned.")
    resp = HttpResponse(status=204)
    return trigger_client_event(resp, "showToast", {"msg": msg, "err": "true"})


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

            query = request.GET.get("query", "")
            sort = request.GET.get("sort", "")
            page = request.GET.get("page", 1)
            month = request.GET.get("month", "")
            year = request.GET.get("year", "")

            # resp = HttpResponse(status=204)
            url = reverse("billings:billings")
            resp = HttpResponseClientRedirect(
                f"{url}?month={month}&year={year}&page={page}&sort={sort}&query={query}"
            )
            msg = _("Selected billings have been deleted.")
            trigger_client_event(resp, "billingsDeleted")
            return trigger_client_event(resp, "showToast", {"msg": msg})
        resp = HttpResponse(status=200)
        return trigger_client_event(resp, "htmx:abort")


#
