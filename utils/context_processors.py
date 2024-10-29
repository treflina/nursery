from datetime import date, timedelta

from django.db.models import Q

from apps.absences.models import Absence
from apps.core.utils.absent_days import get_holidays_in_a_year
from apps.kids.models import Child


def nav_info(request):
    """Context shared between absence views about children presence today
    and tomorrow."""

    info_context = {}
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
        info_context["today_off"] = True
        info_context["tomorrow_off"] = True
        return info_context
    else:
        holiday_days = get_holidays_in_a_year(today.year).values()
        if today in holiday_days:
            info_context["today_off"] = True
        if tomorrow in holiday_days:
            info_context["tomorrow_off"] = True

    num_children_today = Child.objects.filter(
        Q(admission_date__lte=today) & (Q(leave_date__gte=today) | Q(leave_date=None))
    ).count()
    num_children_tomorrow = Child.objects.filter(
        Q(admission_date__lte=tomorrow)
        & (Q(leave_date__gte=tomorrow) | Q(leave_date=None))
    ).count()

    absent_today_qs = Absence.objects.filter(a_date=today).select_related("child")
    absent_today = absent_today_qs.count()
    absent_tomorrow_qs = Absence.objects.filter(a_date=tomorrow).select_related("child")
    absent_tomorrow = absent_tomorrow_qs.count()

    present_today = num_children_today - absent_today
    present_tomorrow = num_children_tomorrow - absent_tomorrow

    try:
        perc_present_today = int(
            ((num_children_today - absent_today) / num_children_today) * 100
        )
        perc_present_tomorrow = int(
            ((num_children_tomorrow - absent_tomorrow) / num_children_tomorrow) * 100
        )
    except ZeroDivisionError:
        perc_present_today = 0
        perc_present_tomorrow = 0

    info_context["today"] = today
    info_context["tomorrow"] = tomorrow
    info_context["absent_today"] = absent_today
    info_context["absent_tomorrow"] = absent_tomorrow
    info_context["absent_today_list"] = absent_today_qs
    info_context["absent_tomorrow_list"] = absent_tomorrow_qs
    info_context["present_today"] = present_today
    info_context["present_tomorrow"] = present_tomorrow
    info_context["perc_present_today"] = perc_present_today
    info_context["perc_present_tomorrow"] = perc_present_tomorrow
    info_context["num_children_today"] = num_children_today
    # print(request.path, info_context)
    return info_context
