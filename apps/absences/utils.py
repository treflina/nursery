from django.conf import settings
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from webpush import send_user_notification

from apps.users.models import Employee


def resp_err(request, template, form):
    """Error response with additional htmx headers."""

    resp = render(request, template, {"form": form})
    resp["HX-Retarget"] = "#absence-errors"
    resp["HX-Reselect"] = "#absence-errors"
    return resp


def send_notification(child, date_from, date_to):
    url = settings.BASE_URL + str(reverse("absences:absences_list"))
    payload = {
        "head": "Nowa nieobecność",
        "body": f"""{child.full_name} od {date_from} do {date_to}. \n
Otwórz zestawienie nieobecności: {url} """,
        "icon": static("favicon/favicon-96x96.png"),
    }
    users = Employee.objects.all()
    for user in users:
        send_user_notification(user=user, payload=payload, ttl=43200)
