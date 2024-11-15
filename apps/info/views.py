from datetime import date

from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView
from django_htmx.http import trigger_client_event

from apps.users.decorators import get_parent_context

from .forms import ActivitiesInfoForm
from .models import Activities, MainTopic, Menu


@get_parent_context
def get_info_about_day(request, selected_child, children, chosendate=None):

    if chosendate is None:
        chosendate = date.today()

    request.session["chosendate"] = chosendate.strftime("%Y-%m-%d")

    menu = Menu.objects.filter(menu_date=chosendate).last()
    activities = Activities.objects.filter(day=chosendate).last()

    context = {
        "menu": menu,
        "activities": activities,
        "chosen_date": chosendate,
        "children": children,
        "selected_child": selected_child,
    }

    response = render(request, template_name="info/infoday.html", context=context)

    return trigger_client_event(
        response,
        "changedDate",
        {"chosendate": chosendate},
        after="swap",
    )


class ActivitiesList(ListView):
    queryset = Activities.objects.all()
    context_object_name = "activities"
    # paginate_by = 10
    template_name = "info/activities_list.html"

    # def get_template_names(self):
    #     if self.request.htmx and (
    #         self.request.headers.get("HX-Target")
    #         not in ["children-main", "children", "children-wrapper"]
    #     ):
    #         template_name = "tables/base_table_partial.html"
    #     else:
    #         template_name = "kids/children_list.html"

    #     return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.db.models import OuterRef, Subquery

        # member_qs = Members.objects.filter(
        #     pk__in = Members.objects.values('designation').distinct().annotate(
        #         pk = Subquery(
        #         Members.objects.filter(
        #             designation= OuterRef("designation")
        #         )
        #         .order_by("pk") # you can set other column, e.g. -pk, create_date...
        #         .values("pk")[:1]
        #         )
        #     )
        # .values_list("pk", flat=True)
        # )
        # get recently updated absence id to set focus
        updated_obj = self.request.session.pop("updated_obj", None)
        context["updated_obj"] = updated_obj
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        created_obj = self.request.session.pop("created_obj", None)
        if created_obj:
            msg = _("New activities have been added")
            return trigger_client_event(response, "showToast", {"msg": msg})
        return response


class ActivityCreateView(CreateView):
    model = Activities
    form_class = ActivitiesInfoForm
    template_name = "info/activity_form.html"
    success_url = reverse_lazy("info:activities_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["creating"] = True
        return context

    def get_success_url(self):
        self.request.session["created_obj"] = True
        return super().get_success_url()
