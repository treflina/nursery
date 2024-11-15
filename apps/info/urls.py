from django.urls import path, register_converter

from apps.core.converters import DateConverter

from .views import ActivitiesList, ActivityCreateView, get_info_about_day

register_converter(DateConverter, "date")

app_name = "info"

urlpatterns = [
    path("informacje/<date:chosendate>/", get_info_about_day, name="day"),
    path("informacje/", get_info_about_day, name="day"),
    path("zajecia/dodaj/", ActivityCreateView.as_view(), name="activity_create"),
    path("zajecia/", ActivitiesList.as_view(), name="activities_list"),
]
