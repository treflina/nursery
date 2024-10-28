from django.urls import path

from .views import create_parent, delete_parent, update_parent

app_name = "users"

urlpatterns = [
    path("profile/create/", create_parent, name="parent_create"),
    path("profile/update/", update_parent, name="parent_update"),
    path("profile/delete/", delete_parent, name="parent_delete"),
]
