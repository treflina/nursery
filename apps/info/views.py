from datetime import date, timedelta
from io import BytesIO

from django.contrib.auth.decorators import user_passes_test
from django.contrib.staticfiles import finders
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView, UpdateView
from django_htmx.http import trigger_client_event
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from apps.users.permissions import (
    EmployeePermissionMixin,
    check_employee,
    login_required_htmx,
)

from .forms import ActivitiesInfoForm, MainTopicForm
from .models import Activities, MainTopic, Menu


def get_info_about_day(request, chosendate=None):

    if chosendate is None:
        chosendate = date.today()

    request.session["chosendate"] = chosendate.strftime("%Y-%m-%d")

    menu = Menu.objects.filter(menu_date=chosendate).last()
    activities = Activities.objects.filter(day=chosendate).last()
    day_before = chosendate - timedelta(days=1)
    next_day = chosendate + timedelta(days=1)

    context = {
        "menu": menu,
        "activities": activities,
        "chosendate": chosendate,
        "day_before": day_before,
        "next_day": next_day,
    }

    response = render(request, template_name="info/infoday.html", context=context)

    return trigger_client_event(
        response,
        "changedDate",
        {"chosendate": chosendate},
        after="swap",
    )


class ActivitiesList(EmployeePermissionMixin, ListView):
    queryset = MainTopic.objects.prefetch_related("activities").all()
    context_object_name = "main_topics"
    # paginate_by = 10

    def get_template_names(self):
        if self.request.htmx and self.request.htmx.target == "activities_list":
            template_name = "info/includes/activities_list.html"
        else:
            template_name = "info/activities.html"
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = MainTopicForm()

        # get recently updated absence id to set focus
        updated_obj = self.request.session.pop("updated_obj", None)
        context["updated_obj"] = updated_obj
        context["form"] = form
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        created_obj = self.request.session.pop("created_obj", None)
        if created_obj:
            msg = _("New activities have been added")
            return trigger_client_event(response, "showToast", {"msg": msg})
        return response


class ActivityCreateView(EmployeePermissionMixin, CreateView):
    model = Activities
    form_class = ActivitiesInfoForm
    template_name = "info/activity_form.html"
    success_url = reverse_lazy("info:activities_list")

    def get(self, request, *args, **kwargs):
        queryset = MainTopic.objects.all()
        pk = self.kwargs.get("pk", None)
        if pk is not None:
            try:
                queryset.get(pk=pk)
            except queryset.model.DoesNotExist:
                raise Http404(_(f"No main topic with id {pk} found."))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["creating"] = True
        redirect_to = self.request.GET.get("next", "")
        context["redirect_to"] = redirect_to
        return context

    def get_success_url(self):
        self.request.session["created_obj"] = True
        return super().get_success_url()

    def form_valid(self, form):
        activity = form.save(commit=False)
        main_topic = MainTopic.objects.get(pk=self.kwargs["pk"])
        activity.main_topic = main_topic
        activity.save()
        return super().form_valid(form)


class ActivityUpdateView(EmployeePermissionMixin, UpdateView):
    model = Activities
    form_class = ActivitiesInfoForm
    template_name = "info/activity_form.html"
    success_url = reverse_lazy("info:activities_list")

    def get_success_url(self):
        url = reverse("info:activities_list")
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


@login_required_htmx
@user_passes_test(check_employee)
@require_http_methods(["DELETE"])
def delete_activity(request, pk):
    if request.htmx:
        activity_to_delete = Activities.objects.filter(pk=pk).last()
        if activity_to_delete:
            activity_to_delete.delete()

            resp = HttpResponse("")
            msg = _("Activity has been deleted.")
            return trigger_client_event(resp, "showToast", {"msg": msg})
        resp = HttpResponse(status=200)
        return trigger_client_event(resp, "htmx:abort")


@login_required_htmx
@user_passes_test(check_employee)
def main_topic_create(request):
    context = {}
    form = MainTopicForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("info:activities_list"))

    context["form"] = form
    return render(request, "info/main_topic_form.html", context)


@login_required_htmx
@user_passes_test(check_employee)
def main_topic_update(request, pk):
    obj = MainTopic.objects.get(id=pk)
    form = MainTopicForm(instance=obj)
    if request.method == "POST":
        form = MainTopicForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # resp = HttpResponse(status=204)
            return redirect(reverse("info:activities_list"))
    return render(
        request,
        "info/main_topic_update.html",
        {"form2": form, "object": obj, "update_main_topic": True},
    )


@login_required_htmx
@user_passes_test(check_employee)
@require_http_methods(["DELETE"])
def delete_main_topic(request, pk):
    if request.htmx:
        main_topic_to_delete = MainTopic.objects.filter(pk=pk).last()
        if main_topic_to_delete:
            main_topic_to_delete.delete()

            resp = HttpResponse("")
            msg = _("Week's activities description has been deleted.")
            return trigger_client_event(resp, "showToast", {"msg": msg})
        resp = HttpResponse(status=200)
        return trigger_client_event(resp, "htmx:abort")


@login_required_htmx
@user_passes_test(check_employee)
def get_pdf(request, pk):

    font_normal = finders.find("fonts/Roboto-Regular.ttf")
    font_medium = finders.find("fonts/Roboto-Medium.ttf")

    pdfmetrics.registerFont(TTFont("roboto", font_normal))
    pdfmetrics.registerFont(TTFont("roboto-medium", font_medium))
    pdfmetrics.registerFontFamily("roboto", normal="roboto", bold="roboto-medium")

    stylesheet = getSampleStyleSheet()
    # headingStyle = stylesheet["Normal"]
    # headingStyle.fontName = "roboto-medium"
    normalStyle = stylesheet["Normal"]
    normalStyle.fontName = "roboto"


    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=landscape(A4),
        rightMargin=50,
        leftMargin=50,
        topMargin=30,
        bottomMargin=30,
    )
    style = ParagraphStyle(
        name="Title",
        fontName="roboto-medium",
        fontSize=12,
        alignment=TA_CENTER,
    )

    topic = MainTopic.objects.get(id=pk)
    activities = topic.activities.all().order_by("day")
    first_date = activities.first()
    if first_date:
        first_day = f"{first_date.day.day}"

    last_date = activities.last()
    if last_date:
        last_day = f"{last_date.day.day}.{last_date.day.month}.{last_date.day.year}"

    if first_date and last_date and first_date != last_date:
        week_dates = first_day + "-" + last_day
    elif last_date:
        week_dates = last_day
    else:
        week_dates = ""

    data = [
        [
            "Temat dnia",
            Paragraph("<b>Aktywność i działalność dziecka</b>", normalStyle),
            "Aktywność ruchowa",
            "Aktywność muzyczna",
            "Aktywność plastyczna",
        ]
    ]
    if any(x.other != "" for x in activities):
        for i, a in enumerate(activities):
            a_topic = f"<b>Dzień {i+1}</b>: {a.topic}" if a.topic else f"<b>Dzień {i+1}</b>"
            activity_data = [
                Paragraph(a_topic, normalStyle),
                Paragraph(a.activity, normalStyle),
                Paragraph(a.movement, normalStyle),
                Paragraph(a.music, normalStyle),
                Paragraph(a.art, normalStyle),
                Paragraph(a.other, normalStyle),
            ]
            data.append(activity_data)

        table = Table(
            data, spaceBefore=20, colWidths=[45 * mm, 45 * mm, 45 * mm, 45 * mm, 45 * mm, 45 * mm]
        )
    else:
        for i, a in enumerate(activities):
            a_topic = f"<b>Dzień {i+1}</b>: {a.topic}" if a.topic else f"<b>Dzień {i+1}</b>"
            activity_data = [
                Paragraph(a_topic, normalStyle),
                Paragraph(a.activity, normalStyle),
                Paragraph(a.movement, normalStyle),
                Paragraph(a.music, normalStyle),
                Paragraph(a.art, normalStyle),
            ]
            data.append(activity_data)

        table = Table(
            data, spaceBefore=20, colWidths=[45 * mm, 57 * mm, 57 * mm, 57 * mm, 57 * mm]
        )

    elems = []
    elems.append(Paragraph((f"Tematyka tygodnia: {topic.description}"), style=style))
    elems.append(Spacer(1, 8))

    if week_dates:
        elems.append(
            Paragraph((f"{week_dates} r."), style=style),
        )
    elems.append(table)
    style_table = TableStyle(
        [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "roboto-medium"),
            ("FONTNAME", (1, -1), (-1, 1), "roboto"),
        ]
    )
    table.setStyle(style_table)
    doc.build(elems)

    pdf_buffer.seek(0)
    return FileResponse(
        pdf_buffer, as_attachment=False, filename=f"tematyka{week_dates}.pdf"
    )
