import calendar
from datetime import date, datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import ProtectedError
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django_htmx.http import reswap, retarget, trigger_client_event

from apps.absences.models import Absence
from apps.billings.models import Billing
from apps.info.models import Activities, Menu
from apps.kids.models import Child
from apps.users.decorators import get_parent_context
from apps.users.models import Parent
from apps.users.permissions import check_employee, check_parent

from .forms import (
    AdditionalDayOffForm,
    FoodPriceForm,
    GovernmentSubsidyForm,
    LocalSubsidyForm,
    MonthlyPaymentForm,
    OtherSubsidyForm,
)
from .models import (
    AdditionalDayOff,
    FoodPrice,
    GovernmentSubsidy,
    LocalSubsidy,
    MonthlyPayment,
    OtherSubsidy,
)
from .utils.absent_days import get_holidays, get_not_enrolled_days
from .utils.helpers import get_next_prev_month


@login_required
@get_parent_context
def home(request, selected_child, children):

    parent = Parent.objects.filter(id=request.user.id).last()

    if request.method == "POST":
        child = request.POST.get("child")
        child_obj = Child.objects.filter(id=child).last()
        if child_obj.parent.id is parent.id:
            selected_child = child_obj.id
            request.session["child"] = selected_child

    return render(
        request,
        template_name="core/home.html",
        context={"children": children, "selected_child": selected_child},
    )


@user_passes_test(check_parent)
@get_parent_context
def day_details(request, selected_child, children, chosendate=None):

    if chosendate is None:
        session_chosendate = request.session.get("chosendate")
        if session_chosendate is None:
            chosendate = date.today()
        else:
            chosendate = datetime.strptime(session_chosendate, "%Y-%m-%d").date()
    else:
        request.session["chosendate"] = chosendate.strftime("%Y-%m-%d")

    menu = Menu.objects.filter(menu_date=chosendate).last()
    activities = Activities.objects.filter(day=chosendate).last()
    context = {
        "chosendate": chosendate,
        "children": children,
        "menu": menu,
        "activities": activities,
    }

    year = chosendate.year
    month = chosendate.month
    day = chosendate.day

    first_day = calendar.monthrange(year, month)[0]
    num_days = calendar.monthrange(year, month)[1]

    cal_months = get_next_prev_month(year, month)
    prev_year = cal_months["previous_year"]
    prev_month = cal_months["previous_month"]

    prev_month_num_days = calendar.monthrange(prev_year, prev_month)[1]

    not_enrolled_days = None

    child = Child.objects.filter(id=selected_child).last()
    if child is not None:
        billing = Billing.objects.filter(
            date_month=date(year, month, 1), child=selected_child, confirmed=True
        ).exists()

        num_days_in_month = num_days
        not_enrolled_days = get_not_enrolled_days(child, year, month)

        enrolled = child.is_enrolled_month(chosendate) and date.today() <= date(
            year, month, num_days
        )

        if num_days_in_month == len(not_enrolled_days):
            anr_days = []
            ar_days = []
            afd_days = []
            ao_days = []
            days_off = []

        else:
            absences_not_reported = Absence.objects.filter(
                child=child, a_date__month=month, a_date__year=year, absence_type="NR"
            )
            absences_reported = Absence.objects.filter(
                child=child, a_date__month=month, a_date__year=year, absence_type="R"
            )
            absences_first_day = Absence.objects.filter(
                child=child, a_date__month=month, a_date__year=year, absence_type="FR"
            )
            absences_other = Absence.objects.filter(
                child=child, a_date__month=month, a_date__year=year, absence_type="O"
            )

            anr_days = [absence.a_date.day for absence in absences_not_reported]
            ar_days = [absence.a_date.day for absence in absences_reported]
            afd_days = [absence.a_date.day for absence in absences_first_day]
            ao_days = [absence.a_date.day for absence in absences_other]

            days_off = get_holidays(year, month)[0]

        context.update(
            {
                "days_off": days_off,
                "year": year,
                "month": month,
                "day": day,
                "displayed_month": date(year, month, 1),
                "prev_year": prev_year,
                "prev_month": prev_month,
                "prev_month_num_days": prev_month_num_days,
                "next_month": cal_months["next_month"],
                "next_year": cal_months["next_year"],
                "num_days": range(1, num_days + 1),
                "first_day": first_day,
                "absences_fdr": afd_days,
                "absences_r": ar_days,
                "absences_nr": anr_days,
                "absences_o": ao_days,
                "not_enrolled": not_enrolled_days,
                "enrolled": enrolled,
                "billing": billing,
            }
        )

    return render(request, "core/base-day.html", context=context)


@user_passes_test(check_employee)
def main_settings(request):
    today = date.today()
    additional_days_off = AdditionalDayOff.objects.filter(day__year__gte=today.year)

    context = {}
    context["monthly_payments"] = MonthlyPayment.objects.all()
    context["local_subsidy"] = LocalSubsidy.objects.last()
    context["local_count"] = LocalSubsidy.objects.count()
    context["government_subsidies"] = GovernmentSubsidy.objects.all()
    context["other_subsidies"] = OtherSubsidy.objects.all()
    context["additional_days_off"] = additional_days_off
    context["food_prices"] = FoodPrice.objects.all()

    return render(request, "core/settings.html", context=context)


@user_passes_test(check_employee)
def create_additional_day_off(request):
    if request.method == "POST":
        form = AdditionalDayOffForm(request.POST)
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            msg = _("Additional day off has been saved.")
            trigger_client_event(resp, "dayOffAdded")
            return trigger_client_event(resp, "showToast", {"msg": msg})
    else:
        form = AdditionalDayOffForm()
    return render(request, "core/settings_form.html", {"form": form, "add": True})


@user_passes_test(check_employee)
@require_http_methods(["DELETE"])
def delete_additional_day_off(request, pk):
    if request.htmx:
        AdditionalDayOff.objects.filter(pk=pk).delete()
        resp = HttpResponse("")
        msg = _("Day off has been deleted.")
        return trigger_client_event(resp, "showToast", {"msg": msg})


@user_passes_test(check_employee)
def create_food_price(request):
    if request.method == "POST":
        form = FoodPriceForm(request.POST)
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            msg = _("Food price has been added.")
            trigger_client_event(resp, "foodPriceAdded")
            return trigger_client_event(resp, "showToast", {"msg": msg})
    else:
        form = FoodPriceForm()
    return render(
        request, "core/settings_form.html", {"form": form, "add_food_price": True}
    )


@user_passes_test(check_employee)
@require_http_methods(["DELETE"])
def delete_food_price(request, pk):
    if request.htmx:
        try:
            FoodPrice.objects.filter(pk=pk).delete()
            resp = HttpResponse("")
            msg = _("Food price has been deleted.")
            return trigger_client_event(resp, "showToast", {"msg": msg})
        except ProtectedError:
            resp = HttpResponse(
                """<p id='msg'>You can't delete the food price already assigned
                to a child. You can change only the price instead.</p>"""
            )
            resp["HX-Reselect"] = "#msg"
            reswap(resp, "innerHTML")
            return retarget(resp, "#messages-box")


@user_passes_test(check_employee)
def update_food_price(request, pk):
    obj = FoodPrice.objects.get(id=pk)

    form = FoodPriceForm(instance=obj)
    if request.method == "POST":
        form = FoodPriceForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            return trigger_client_event(resp, "foodPriceChanged")
    return render(
        request, "core/settings_form.html", {"form": form, "update_food_price": True}
    )


@user_passes_test(check_employee)
def create_monthly_payment(request):
    if request.method == "POST":
        form = MonthlyPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            msg = _("Monthly payment has been added.")
            trigger_client_event(resp, "paymentChanged")
            return trigger_client_event(resp, "showToast", {"msg": msg})
    else:
        form = MonthlyPaymentForm()
    return render(
        request, "core/settings_form.html", {"form": form, "add_monthly": True}
    )


@user_passes_test(check_employee)
def update_monthly_payment(request, pk):
    obj = MonthlyPayment.objects.get(id=pk)

    form = MonthlyPaymentForm(instance=obj)
    if request.method == "POST":
        form = MonthlyPaymentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            return trigger_client_event(resp, "paymentChanged")
    return render(
        request,
        "core/settings_form.html",
        {"form": form, "update_monthly_payment": True},
    )


@user_passes_test(check_employee)
@require_http_methods(["DELETE"])
def delete_monthly_payment(request, pk):
    if request.htmx:
        try:
            MonthlyPayment.objects.filter(pk=pk).delete()
            resp = HttpResponse("")
            msg = _("Monthly payment has been deleted.")
            return trigger_client_event(resp, "showToast", {"msg": msg})
        except ProtectedError:
            resp = HttpResponse(
                """<p id='msg'>You can't delete the monthly payment already assigned
                to a child. You can change only the price instead.</p>"""
            )
            resp["HX-Reselect"] = "#msg"
            reswap(resp, "innerHTML")
            return retarget(resp, "#messages-box5")


@user_passes_test(check_employee)
def create_local_subsidy(request):
    if request.method == "POST":
        form = LocalSubsidyForm(request.POST)
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            msg = _("Subsidy has been added.")
            trigger_client_event(resp, "localChanged")
            return trigger_client_event(resp, "showToast", {"msg": msg})
    else:
        form = LocalSubsidyForm()
    return render(request, "core/settings_form.html", {"form": form, "add_local": True})


@user_passes_test(check_employee)
def update_local_subsidy(request, pk):
    obj = LocalSubsidy.objects.get(id=pk)

    form = LocalSubsidyForm(instance=obj)
    if request.method == "POST":
        form = LocalSubsidyForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            return trigger_client_event(resp, "localChanged")
    return render(
        request, "core/settings_form.html", {"form": form, "update_local": True}
    )


@user_passes_test(check_employee)
def update_gov_subsidy(request, pk):
    obj = GovernmentSubsidy.objects.get(id=pk)

    form = GovernmentSubsidyForm(instance=obj)
    if request.method == "POST":
        form = GovernmentSubsidyForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            return trigger_client_event(resp, "govChanged")
    return render(request, "core/settings_form.html", {"form": form, "gov": True})


@user_passes_test(check_employee)
def create_gov_subsidy(request):
    if request.method == "POST":
        form = GovernmentSubsidyForm(request.POST)
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            msg = _("Subsidy has been added.")
            trigger_client_event(resp, "govChanged")
            return trigger_client_event(resp, "showToast", {"msg": msg})
    else:
        form = GovernmentSubsidyForm()
    return render(request, "core/settings_form.html", {"form": form, "gov": True})


@user_passes_test(check_employee)
@require_http_methods(["DELETE"])
def delete_gov_subsidy(request, pk):
    if request.htmx:
        try:
            GovernmentSubsidy.objects.filter(pk=pk).delete()
            resp = HttpResponse("")
            msg = _("Subsidy has been deleted.")
            return trigger_client_event(resp, "showToast", {"msg": msg})
        except ProtectedError:
            resp = HttpResponse(
                """<p id='msg'>You can't delete this subsidy because is still assigned
                to a child. You can change the amount instead.</p>"""
            )
            resp["HX-Reselect"] = "#msg"
            reswap(resp, "innerHTML")
            return retarget(resp, "#messages-box2")


@user_passes_test(check_employee)
def update_other_subsidy(request, pk):
    obj = OtherSubsidy.objects.get(id=pk)

    form = OtherSubsidyForm(instance=obj)
    if request.method == "POST":
        form = OtherSubsidyForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            return trigger_client_event(resp, "otherChanged")
    return render(
        request, "core/settings_form.html", {"form": form, "update_other": True}
    )


@user_passes_test(check_employee)
@require_http_methods(["DELETE"])
def delete_other_subsidy(request, pk):
    if request.htmx:
        try:
            OtherSubsidy.objects.filter(pk=pk).delete()
            resp = HttpResponse("")
            msg = _("Subsidy has been deleted.")
            return trigger_client_event(resp, "showToast", {"msg": msg})
        except ProtectedError:
            resp = HttpResponse(
                """<p id='msg'>You can't delete this subsidy because it's still assigned
                to a child. You can change the amount instead.</p>"""
            )
            resp["HX-Reselect"] = "#msg"
            reswap(resp, "innerHTML")
            return retarget(resp, "#messages-box3")


@user_passes_test(check_employee)
def create_other_subsidy(request):
    if request.method == "POST":
        form = OtherSubsidyForm(request.POST)
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            msg = _("Subsidy has been added.")
            trigger_client_event(resp, "otherChanged")
            return trigger_client_event(resp, "showToast", {"msg": msg})
    else:
        form = OtherSubsidyForm()
    return render(request, "core/settings_form.html", {"form": form, "gov": True})
