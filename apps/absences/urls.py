from django.urls import path

from .views import (
    AbsenceDetailView,
    AbsencesView,
    AbsenceUpdateView,
    create_absence,
    delete_absence,
    nursery_create_absence,
    top_info_about_absences,
)

app_name = "absences"

urlpatterns = [
    path("absence/create/", create_absence, name="absence_create"),
    path(
        "absence/nursery-create/", nursery_create_absence, name="absence_create_nursery"
    ),
    path("absence/<int:pk>", AbsenceDetailView.as_view(), name="absence_detail"),
    path("absence/update/<int:pk>", AbsenceUpdateView.as_view(), name="absence_update"),
    path("absence/delete/<int:pk>", delete_absence, name="absence_delete"),
    path(
        "absences/",
        AbsencesView.as_view(),
        name="absences_list",
    ),
    path("absences/info/", top_info_about_absences, name="absences_top_info"),
]
