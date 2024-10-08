from datetime import date, datetime

from django.shortcuts import render

from apps.billings.models import Billing
from apps.users.decorators import get_parent_context


@get_parent_context
def switch_child_profile(request, selected_child, children):

    ids = sorted([child.id for child in children])
    children_count = children.count()

    selected_child_idx = ids.index(selected_child)

    if ids.index(selected_child) == children_count - 1:
        new_selected_id = ids[0]
    else:
        new_selected_id = ids[selected_child_idx + 1]

    request.session["child"] = new_selected_id

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
        {"chosendate": chosendate, "children": children, "billing": billing},
    )
