from django.urls import path

from .views import (
    delete_absence,
    switch_child_profile,
    ChildrenList,
    ChildCreateView,
    ChildUpdateView,
)

app_name = "kids"

urlpatterns = [
    path("switch", switch_child_profile, name="switch"),
    path("children/", ChildrenList.as_view(), name="children"),
    path("children/delete/<int:pk>/", delete_absence, name="delete"),
    path("children/create", ChildCreateView.as_view(), name="create"),
    path("children/update/<int:pk>/", ChildUpdateView.as_view(), name="update"),
]
