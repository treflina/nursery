from django.urls import path

from .views import switch_child_profile

app_name = "kids"

urlpatterns = [
    path("switch", switch_child_profile, name="switch"),
]
