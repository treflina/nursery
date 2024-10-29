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
    path("children/", ChildrenList.as_view(), name="children"),
    path("children/delete/<int:pk>/", delete_child, name="delete"),
    path("children/create", ChildCreateView.as_view(), name="create"),
    path("children/update/<int:pk>/", ChildUpdateView.as_view(), name="update"),
]
