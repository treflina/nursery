from django.urls import path

from .views import (
    contributions,
    create_contribution,
    delete_contribution,
    update_contribution,
    update_contribution_published,
    update_contribution_status,
)

app_name = "contributions"

urlpatterns = [
    path("skladki/<int:pk>/", contributions, name="contributions"),
    path("skladki/", contributions, name="contributions"),
    path("skladki/dodaj/", create_contribution, name="create"),
    path("skladki/zmien/<int:pk>/", update_contribution, name="update"),
    path("skladki/status/<int:pk>/", update_contribution_status, name="update_paid"),
    path(
        "skladki/widocznosc/<int:pk>/",
        update_contribution_published,
        name="update_published",
    ),
    path("skladki/usun/<int:pk>/", delete_contribution, name="delete"),
]
