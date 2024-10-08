from datetime import date, datetime, timedelta

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, UpdateView
from django_filters.views import FilterView
from django_htmx.http import trigger_client_event
from django_tables2 import SingleTableMixin

from apps.core.utils.absent_days import get_holidays, get_holidays_in_a_year
from apps.core.utils.helpers import daterange
from apps.kids.models import Child
from apps.users.decorators import get_parent_context

from .filters import AbsencesFilter
from .forms import AbsenceForm
from .models import Absence
from .tables import AbsencesTable


class AbsencesView(SingleTableMixin, FilterView):

    table_class = AbsencesTable
    queryset = Absence.objects.all()
    filterset_class = AbsencesFilter
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            template_name = "tables/base_table_partial.html"
        else:
            template_name = "absences/absence_list.html"

        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()

        # check if weekend
        if today.weekday() == 5:
            today = today + timedelta(days=2)
        elif today.weekday() == 6:
            today = today + timedelta(days=1)

        if today.weekday() == 4:
            tomorrow = today + timedelta(days=3)
        else:
            tomorrow = today + timedelta(days=1)

        # check if holiday
        if today.month == 12 and (today.day == 31 or today.day == 25):
            context["today_off"] = True
            context["tomorrow_off"] = True
            return context
        else:
            holiday_days = get_holidays_in_a_year(today.year).values()
            if today in holiday_days:
                context["today_off"] = True
            if tomorrow in holiday_days:
                context["tomorrow_off"] = True

        num_children_today = Child.objects.filter(
            Q(admission_date__lte=today)
            & (Q(leave_date__gte=today) | Q(leave_date=None))
        ).count()
        num_children_tomorrow = Child.objects.filter(
            Q(admission_date__lte=tomorrow)
            & (Q(leave_date__gte=tomorrow) | Q(leave_date=None))
        ).count()

        absent_today_qs = Absence.objects.filter(a_date=today).select_related("child")
        absent_today = absent_today_qs.count()
        absent_tomorrow_qs = Absence.objects.filter(a_date=tomorrow).select_related(
            "child"
        )
        absent_tomorrow = absent_tomorrow_qs.count()

        present_today = num_children_today - absent_today
        present_tomorrow = num_children_tomorrow - absent_tomorrow

        try:
            perc_present_today = int(
                ((num_children_today - absent_today) / num_children_today) * 100
            )
            perc_present_tomorrow = int(
                ((num_children_tomorrow - absent_tomorrow) / num_children_tomorrow)
                * 100
            )
        except ZeroDivisionError:
            perc_present_today = 0
            perc_present_tomorrow = 0

        context["today"] = today
        context["tomorrow"] = tomorrow
        context["absent_today"] = absent_today
        context["absent_tomorrow"] = absent_tomorrow
        context["absent_today_list"] = absent_today_qs
        context["absent_tomorrow_list"] = absent_tomorrow_qs
        context["present_today"] = present_today
        context["present_tomorrow"] = present_tomorrow
        context["perc_present_today"] = perc_present_today
        context["perc_present_tomorrow"] = perc_present_tomorrow

        return context


class AbsenceDetailView(DetailView):
    model = Absence
    template_name = "absences/absence_detail.html"
    # context_object_name = "absence"


class AbsenceUpdateView(SuccessMessageMixin, UpdateView):
    model = Absence
    fields = ["reason", "absence_type"]
    template_name = "absences/absence_update.html"
    success_url = reverse_lazy("absences:absences_list")
    success_message = _("Data has been successfully changed")


@get_parent_context
def create_absence(request, selected_child, children, chosendate=None):
    if request.method == "POST":
        form = AbsenceForm(request.POST)

        if form.is_valid():
            date_from = form.cleaned_data.get("a_date")
            date_to = form.cleaned_data.get("date_to")
            reason = form.cleaned_data.get("reason")
            # TODO: Absences longer than 2 months should be
            # reported directly to nursery

            days_off = get_holidays(date_from.year, date_from.month)[1]

            child = None
            if selected_child:
                child = Child.objects.get(id=selected_child)

            if child:
                if date_from.month != date_to.month:
                    days_off += get_holidays(date_to.year, date_to.month)[1]

                if date_from != date_to:
                    for day in daterange(date_from + timedelta(days=1), date_to):
                        if day not in days_off:
                            abs = Absence(
                                child=child, a_date=day, reason=reason, absence_type="R"
                            )
                            abs.save()
                # TODO form validate first day if it's not in days off
                first_day_absence = Absence(
                    child=child, a_date=date_from, reason=reason, absence_type="FR"
                )
                first_day_absence.save()

                resp = render(
                    request,
                    "core/base-day.html",
                    context={"chosendate": date_from, "form": AbsenceForm()},
                )
                return trigger_client_event(resp, "success", after="settle")

            return HttpResponse(
                "<h3>Przepraszamy, ale nie znaleźliśmy dziecka przypisanego \
                    do Twojego konta.</h3>"
            )

    else:
        chosendate = request.session.get("chosendate")

        if chosendate is None:
            chosendate = date.today()
        else:
            chosendate = datetime.strptime(chosendate, "%Y-%m-%d").date()

        form = AbsenceForm()

    child = Child.objects.filter(id=selected_child).last()

    resp = render(
        request,
        "core/includes/absence-modal.html",
        {"form": form, "chosendate": chosendate, "child": child},
    )
    return trigger_client_event(resp, "createDatepickerForm", after="settle")
