from django.urls import path

from .views import (
    ChildCreateView,
    ChildrenList,
    ChildUpdateView,
    delete_child,
    switch_child_profile,
)

app_name = "kids"

urlpatterns = [
    path("switch", switch_child_profile, name="switch"),
    path("dzieci/", ChildrenList.as_view(), name="children"),
    path("dzieci/usun/<int:pk>/", delete_child, name="delete"),
    path("dzieci/dodaj", ChildCreateView.as_view(), name="create"),
    # path("children/create", create_child, name="create"),
    path("dzieci/edytuj/<int:pk>/", ChildUpdateView.as_view(), name="update"),
]
