from django.urls import path

from .views import (
    AbsenceDetailView,
    AbsenceDeleteView,
    AbsencesView,
    AbsenceUpdateView,
    create_absence,
)

app_name = "absences"

urlpatterns = [
    path("absence/create/", create_absence, name="absence_create"),
    path("absence/<int:pk>", AbsenceDetailView.as_view(), name="absence_detail"),
    path("absence/update/<int:pk>", AbsenceUpdateView.as_view(), name="absence_update"),
    path("absence/delete/<int:pk>", AbsenceDeleteView.as_view(), name="absence_delete"),
    path(
        "absences/",
        AbsencesView.as_view(),
        name="absences_list",
    ),
]
