import calendar
from datetime import date, datetime

from django.shortcuts import render
from django.views.generic import CreateView

from apps.absences.models import Absence
from apps.billings.models import Billing
from apps.kids.models import Child
from apps.users.decorators import get_parent_context
from apps.users.models import Parent

from .models import FoodPrice
from .utils.absent_days import get_holidays, get_not_enrolled_days
from .utils.helpers import get_next_prev_month


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


@get_parent_context
def display_calendar(
    request, selected_child, children, year=None, month=None, day=None
):
    """Display calendar"""

    if month is None:
        month = date.today().month
    if year is None:
        year = date.today().year
    if day is None:
        day = date.today().day

    first_day = calendar.monthrange(year, month)[0]
    num_days = calendar.monthrange(year, month)[1]

    cal_months = get_next_prev_month(year, month)
    prev_year = cal_months["previous_year"]
    prev_month = cal_months["previous_month"]

    prev_month_num_days = calendar.monthrange(prev_year, prev_month)[1]

    child = None
    not_enrolled_days = None
    if selected_child:
        child = Child.objects.get(id=selected_child)
        not_enrolled_days = get_not_enrolled_days(child, year, month)

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

    context = {
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
    }

    return render(request, "core/calendar.html", context=context)


@get_parent_context
def day_details(request, selected_child, children, chosendate=None):

    if chosendate is None:
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
        context={
            "chosendate": chosendate,
            "children": children,
            "billing": billing,
        },
    )

def main_settings(self):
    pass


class FoodPrice(CreateView):
    model = FoodPrice
    template_name = "core/foodprice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = self.model.objects.all()
        return context