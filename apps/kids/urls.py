from django.urls import path

from .views import switch_child_profile, ChildrenList, ChildCreateView

app_name = "kids"

urlpatterns = [
    path("switch", switch_child_profile, name="switch"),
    path("children/", ChildrenList.as_view(), name="children"),
    path("children/create", ChildCreateView.as_view(), name="child_create"),
]
