from django.urls import path

from .views import (
    AbsencesView,
    AbsenceUpdateView,
    create_absence,
    delete_absence,
    nursery_create_absence,
    top_info_about_absences,
)

app_name = "absences"

urlpatterns = [
    path("nieobecnosc/dodaj/", create_absence, name="absence_create"),
    path(
        "nieobecnosc/zlobek-create/",
        nursery_create_absence,
        name="absence_create_nursery",
    ),
    path(
        "nieobecnosc/edytuj/<int:pk>",
        AbsenceUpdateView.as_view(),
        name="absence_update",
    ),
    path("nieobecnosc/usun/<int:pk>", delete_absence, name="absence_delete"),
    path(
        "nieobecnosci/",
        AbsencesView.as_view(),
        name="absences_list",
    ),
    path("nieobecnosci/info/", top_info_about_absences, name="absences_top_info"),
]
