from datetime import date

from django.shortcuts import render
from django_htmx.http import trigger_client_event

from apps.users.decorators import get_parent_context

from .models import Activities, Menu


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
