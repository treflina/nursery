from django.urls import path, register_converter

from .converters import DateConverter
from .views import (
    create_additional_day_off,
    create_food_price,
    create_gov_subsidy,
    create_local_subsidy,
    create_monthly_payment,
    create_other_subsidy,
    day_details,
    delete_additional_day_off,
    delete_food_price,
    delete_gov_subsidy,
    delete_monthly_payment,
    delete_other_subsidy,
    home,
    main_settings,
    update_food_price,
    update_gov_subsidy,
    update_local_subsidy,
    update_monthly_payment,
    update_other_subsidy,
)

register_converter(DateConverter, "date")

app_name = "core"

urlpatterns = [
    path("promyczki/<date:chosendate>/", day_details, name="day"),
    path("promyczki/", day_details, name="day"),
    path("ustawienia/", main_settings, name="settings"),
    path("ustawienia/createday/", create_additional_day_off, name="day_create"),
    path(
        "ustawienia/deleteday/<int:pk>/", delete_additional_day_off, name="day_delete"
    ),
    path("ustawienia/createfoodprice/", create_food_price, name="food_price_create"),
    path(
        "ustawienia/deletefoodprice/<int:pk>/",
        delete_food_price,
        name="food_price_delete",
    ),
    path(
        "ustawienia/updatefoodprice/<int:pk>/",
        update_food_price,
        name="food_price_update",
    ),
    path(
        "ustawienia/createmonthlypayment/",
        create_monthly_payment,
        name="monthly_payment_create",
    ),
    path(
        "ustawienia/updatemonthlypayment/<int:pk>/",
        update_monthly_payment,
        name="monthly_payment_update",
    ),
    path(
        "ustawienia/deletemonthlypayment/<int:pk>/",
        delete_monthly_payment,
        name="monthly_payment_delete",
    ),
    path(
        "ustawienia/createlocalsubsidy/",
        create_local_subsidy,
        name="local_subsidy_create",
    ),
    path(
        "ustawienia/updatelocalsubsidy/<int:pk>/",
        update_local_subsidy,
        name="local_subsidy_update",
    ),
    path(
        "ustawienia/createothersubsidy/",
        create_other_subsidy,
        name="other_subsidy_create",
    ),
    path(
        "ustawienia/deleteothersubsidy/<int:pk>/",
        delete_other_subsidy,
        name="other_subsidy_delete",
    ),
    path(
        "ustawienia/updateothersubsidy/<int:pk>/",
        update_other_subsidy,
        name="other_subsidy_update",
    ),
    path(
        "ustawienia/updategovsubsidy/<int:pk>/",
        update_gov_subsidy,
        name="gov_subsidy_update",
    ),
    path("ustawienia/creategovsubsidy/", create_gov_subsidy, name="gov_subsidy_create"),
    path(
        "ustawienia/deletegovsubsidy/<int:pk>/",
        delete_gov_subsidy,
        name="gov_subsidy_delete",
    ),
    path("", home, name="home"),
]
