import calendar
from datetime import date, timedelta

from dateutil import easter
from dateutil.relativedelta import TH, relativedelta

from apps.absences.models import Absence

from ..models import AdditionalDayOff


def get_holidays_in_a_year(year):
    """Returns Polish holidays dates (legally considered non-working days)"""
    easter_sunday = easter.easter(year)
    holidays = {
        "New Year": date(year, 1, 1),
        "Trzech Kroli": date(year, 1, 6),
        "Easter Sunday": easter_sunday,
        "Easter Monday": easter_sunday + timedelta(days=1),
        "Labor Day": date(year, 5, 1),
        "Constitution Day": date(year, 5, 3),
        # 9th Thursday after Easter
        "Corpus Christi": easter_sunday + relativedelta(weekday=TH(+9)),
        "Assumption of the Blessed Virgin Mary": date(year, 8, 15),
        "All Saints' Day": date(year, 11, 1),
        "Independence Day": date(year, 11, 11),
        "Christmas  Day": date(year, 12, 25),
        "Boxing Day": date(year, 12, 26),
    }
    additional_days_off = AdditionalDayOff.objects.filter(day__year=year)
    additional_days_off_dict = {k: v.day for (k, v) in enumerate(additional_days_off)}
    holidays.update(additional_days_off_dict)
    return holidays


def get_holidays(year, month):
    holidays = get_holidays_in_a_year(year)
    holidays_days = holidays.values()
    holidays_per_month = list(filter(lambda x: x.month == month, holidays_days))

    days_range = calendar.monthrange(year, month)[1]
    weekends = []
    for day in range(1, days_range + 1):
        d = date(year, month, day)
        if d.weekday() in [5, 6]:
            weekends.append(d)
    holidays_weekends = list(set(weekends + holidays_per_month))

    days_off = [int(d.day) for d in holidays_weekends]
    return (days_off, holidays_weekends)


def get_not_enrolled_days(child, year, month):

    num_days_in_month = calendar.monthrange(year, month)[1]
    last_day = date(year, month, num_days_in_month)
    last_month_end = date(year, month, 1) - timedelta(days=1)

    if child.leave_date and child.leave_date <= last_month_end:
        return range(1, num_days_in_month + 1)

    if child.admission_date and child.admission_date > last_day:
        return range(1, num_days_in_month + 1)

    if (
        child.admission_date
        and child.admission_date.month == month
        and child.admission_date.day != 1
    ):
        days_before_admission = [
            int(d) for d in range(1, int(child.admission_date.day))
        ]
    else:
        days_before_admission = []
    if (
        child.leave_date is not None
        and child.leave_date.month == month
        and child.leave_date.day != num_days_in_month
    ):
        days_after_leave = [
            int(d) for d in range(int(child.leave_date.day) + 1, num_days_in_month + 1)
        ]
    else:
        days_after_leave = []
    return days_after_leave + days_before_admission


def get_child_absent_days(child, year, month):

    not_enrolled_days = get_not_enrolled_days(child, year, month)
    absences_reported = Absence.objects.get_absence_child_month(child, year, month)
    absences_reported_days = [int(a.a_date.day) for a in absences_reported]

    absences = list(set(not_enrolled_days + absences_reported_days))

    return absences


def get_all_absent_days(child, year, month):
    child_absences = get_child_absent_days(child, year, month)
    holidays = get_holidays(year, month)[0]
    return list(set(child_absences + holidays))
