from django.urls import path, register_converter

from apps.core.converters import DateConverter

from .views import (
    ActivitiesList,
    ActivityCreateView,
    ActivityUpdateView,
    delete_activity,
    delete_main_topic,
    get_info_about_day,
    get_pdf,
    main_topic_create,
    main_topic_update,
)

register_converter(DateConverter, "date")

app_name = "info"

urlpatterns = [
    path("informacje/<date:chosendate>/", get_info_about_day, name="day"),
    path("informacje/", get_info_about_day, name="day"),
    path("opistygodnia/dodaj/", main_topic_create, name="topic_create"),
    path("opistygodnia/zmien/<int:pk>/", main_topic_update, name="main_topic_update"),
    path("opistygodnia/usun/<int:pk>/", delete_main_topic, name="main_topic_delete"),
    path(
        "zajecia/dodaj/<int:pk>/", ActivityCreateView.as_view(), name="activity_create"
    ),
    path(
        "zajecia/zmien/<int:pk>/", ActivityUpdateView.as_view(), name="activity_update"
    ),
    path("zajecia/usun/<int:pk>/", delete_activity, name="activity_delete"),
    path("zajecia/", ActivitiesList.as_view(), name="activities_list"),
    path("pdf/<int:pk>/", get_pdf, name="get_pdf"),
]
