import logging
from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import UpdateView
from django_filters.views import FilterView
from django_htmx.http import trigger_client_event
from django_tables2 import SingleTableMixin

from apps.core.utils.absent_days import get_holidays
from apps.core.utils.helpers import daterange
from apps.kids.models import Child
from apps.users.decorators import get_parent_context
from apps.users.permissions import (
    EmployeePermissionMixin,
    check_employee,
    check_parent,
    check_staff,
    login_required_htmx,
)

from .filters import AbsencesFilter
from .forms import AbsenceForm, NurseryAbsenceForm, UpdateAbsenceForm
from .models import Absence
from .tables import AbsencesTable
from .utils import resp_err, send_notification

logger = logging.getLogger("django")


class AbsencesView(EmployeePermissionMixin, SingleTableMixin, FilterView):

    table_class = AbsencesTable
    queryset = Absence.objects.all().order_by("-created_at")
    filterset_class = AbsencesFilter
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx and (
            self.request.headers.get("HX-Target") not in ["absences-main", "body"]
        ):
            template_name = "tables/base_table_partial.html"
        else:
            template_name = "absences/absences_list.html"

        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get recently updated absence id to set focus
        updated_obj = self.request.session.pop("updated_obj", None)
        context["updated_obj"] = updated_obj
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        created_abs = self.request.session.pop("created_absence", None)
        if created_abs:
            msg = _("Absence has been added.")
            trigger_client_event(response, "updateTopNav")
            return trigger_client_event(response, "showToast", {"msg": msg})

        return response


@login_required_htmx
@user_passes_test(check_staff)
def top_info_about_absences(request):

    resp = render(request, "absences/includes/absences_top_info.html")
    resp["HX-Trigger"] = "get_top_info"
    return resp


class AbsenceUpdateView(EmployeePermissionMixin, UpdateView):
    model = Absence
    form_class = UpdateAbsenceForm
    template_name = "absences/absence_update.html"
    # success_message = _("Data has been successfully changed")

    def get_success_url(self):
        self.request.session["updated_obj"] = self.kwargs.get("pk")
        url = reverse("absences:absences_list")
        if "next" in self.request.GET:
            url = self.request.GET["next"]
        return url


@login_required_htmx
@user_passes_test(check_employee)
@require_http_methods(["DELETE"])
def delete_absence(request, pk):
    if request.htmx:
        Absence.objects.filter(pk=pk).delete()
        return HttpResponse("", headers={"HX-Trigger": "absenceDeleted"})


@login_required_htmx
@user_passes_test(check_parent)
@get_parent_context
def create_absence(request, selected_child, children, chosendate=None):

    child = None
    if selected_child:
        child = Child.objects.filter(id=selected_child).last()

    if not child:
        return HttpResponse(
            "<h3>Przepraszamy, ale nie znaleźliśmy dziecka przypisanego \
                    do Twojego konta.</h3>"
        )

    if request.method == "POST":
        form = AbsenceForm(request.POST)

        if form.is_valid():
            date_from = form.cleaned_data.get("a_date")
            date_to = form.cleaned_data.get("date_to")
            reason = form.cleaned_data.get("reason")

            if (child.leave_date and child.leave_date < date_to) or (
                child.admission_date and child.admission_date > date_from
            ):
                form.add_error(
                    None,
                    _(_("The child doesn't attent nursery in this period.")),
                )
                return resp_err(request, "absences/includes/absence_form.html", form)

            days_off = get_holidays(date_from.year, date_from.month)[1]

            if date_from.month != date_to.month:
                days_off += get_holidays(date_to.year, date_to.month)[1]

            days_range = daterange(date_from, date_to + timedelta(days=1))

            absences_list = []

            for idx, day in enumerate(days_range):
                if Absence.objects.filter(child=child, a_date=day).exists():
                    form.add_error(
                        None,
                        _(
                            "Check if there hasn't already been reported an absence \
for the submitted date."
                        ),
                    )
                    return resp_err(
                        request, "absences/includes/absence_form.html", form
                    )

                if day not in days_off:
                    now = datetime.now()
                    today8am = now.replace(hour=8, minute=2, second=0, microsecond=0)

                    if not idx and day == now.date() and now > today8am:
                        absence = Absence(
                            child=child, a_date=day, reason=reason, absence_type="FR"
                        )
                        absences_list.append(absence)

                    else:
                        absence = Absence(
                            child=child, a_date=day, reason=reason, absence_type="R"
                        )
                        absences_list.append(absence)

            if absences_list:
                Absence.objects.bulk_create(absences_list)
                try:
                    send_notification(child, date_from, date_to)
                except Exception as e:
                    logger.error(f"{e}")
                msg = _("Absence has been successfully submitted")
                resp = HttpResponse(status=204)
                trigger_client_event(resp, "showToast", {"msg": msg})
                return trigger_client_event(resp, "absenceAdded")
            else:
                form.add_error(None, _("Chosen days are already off."))
                return resp_err(request, "absences/includes/absence_form.html", form)
        else:
            return resp_err(request, "absences/includes/absence_form.html", form)

    else:
        chosendate = request.session.get("chosendate")
        if chosendate is None:
            chosendate = date.today()
        else:
            chosendate = datetime.strptime(chosendate, "%Y-%m-%d").date()

        form = AbsenceForm()

    resp = render(
        request,
        "absences/includes/absence_form.html",
        {"form": form, "chosendate": chosendate, "child": child},
    )
    return trigger_client_event(resp, "createAbsenceForm", after="settle")


@login_required_htmx
@user_passes_test(check_employee)
def nursery_create_absence(request):

    if request.method == "POST":
        form = NurseryAbsenceForm(request.POST)

        if form.is_valid():
            date_from = form.cleaned_data.get("a_date")
            date_to = form.cleaned_data.get("date_to")
            reason = form.cleaned_data.get("reason")
            child = form.cleaned_data.get("child")
            absence_type = form.cleaned_data.get("absence_type")
            first_day_paid = form.cleaned_data.get("first_day_paid")

            days_off = get_holidays(date_from.year, date_from.month)[1]

            if date_from.month != date_to.month:
                days_off += get_holidays(date_to.year, date_to.month)[1]

            days_range = daterange(date_from, date_to + timedelta(days=1))

            absences_list = []

            for idx, day in enumerate(days_range):
                if Absence.objects.filter(child=child, a_date=day).exists():
                    form.add_error(
                        None,
                        _(
                            "Check if there hasn't already been reported an absence \
for the submitted date."
                        ),
                    )
                    return resp_err(
                        request, "absences/includes/absence_form_nursery.html", form
                    )

                if day not in days_off:
                    if not idx and first_day_paid:
                        absence = Absence(
                            child=child, a_date=day, reason=reason, absence_type="FR"
                        )
                        absences_list.append(absence)
                    else:
                        absence = Absence(
                            child=child,
                            a_date=day,
                            reason=reason,
                            absence_type=absence_type,
                        )
                        absences_list.append(absence)

            if absences_list:
                Absence.objects.bulk_create(absences_list)
                request.session["created_absence"] = True
                return redirect(reverse("absences:absences_list"))
            else:
                form.add_error(None, _("Chosen days are already off."))
                return resp_err(
                    request, "absences/includes/absence_form_nursery.html", form
                )
        else:
            return resp_err(
                request, "absences/includes/absence_form_nursery.html", form
            )

    else:
        form = NurseryAbsenceForm()

    resp = render(
        request,
        "absences/includes/absence_form_nursery.html",
        {"form": form},
    )
    return trigger_client_event(resp, "createAbsenceForm", after="settle")
