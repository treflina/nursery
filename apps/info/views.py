from datetime import date

from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView, UpdateView
from django_htmx.http import trigger_client_event

from apps.users.decorators import get_parent_context

from .forms import ActivitiesInfoForm, MainTopicForm
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


class ActivityCreateView(CreateView):
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


class ActivityUpdateView(UpdateView):
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


def main_topic_create(request):
    context = {}
    form = MainTopicForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("info:activities_list"))

    context["form"] = form
    return render(request, "info/main_topic_form.html", context)


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
