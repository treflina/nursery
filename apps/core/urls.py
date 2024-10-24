from django.urls import path, register_converter

from .converters import DateConverter
from .views import day_details, display_calendar, home

register_converter(DateConverter, "date")

app_name = "core"

urlpatterns = [
    path(
        "calendar/<int:year>/<int:month>/<int:day>/", display_calendar, name="calendar"
    ),
    path("calendar/<int:year>/<int:month>/", display_calendar, name="calendar"),
    path("calendar/", display_calendar, name="calendar"),
    path("day/<date:chosendate>/", day_details, name="day"),
    path("day/", day_details, name="day"),
    path("settings/", day_details, name="settings"),
    path("", home, name="home"),
]
