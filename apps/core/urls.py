from django.urls import path, register_converter

from .converters import DateConverter
from .views import (
    create_additional_day_off,
    create_food_price,
    day_details,
    delete_additional_day_off,
    delete_food_price,
    display_calendar,
    home,
    main_settings,
    update_food_price,
)

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
    path("settings/", main_settings, name="settings"),
    path("settings/createday/", create_additional_day_off, name="day_create"),
    path("settings/deleteday/<int:pk>/", delete_additional_day_off, name="day_delete"),
    path("settings/createfoodprice/", create_food_price, name="food_price_create"),
    path(
        "settings/deletefoodprice/<int:pk>/",
        delete_food_price,
        name="food_price_delete",
    ),
    path(
        "settings/updatefoodprice/<int:pk>/",
        update_food_price,
        name="food_price_update",
    ),
    path("", home, name="home"),
]
