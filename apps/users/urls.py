from django.urls import path

from .views import (
    change_email_parent,
    change_password_parent,
    create_parent,
    delete_parent,
)

app_name = "users"

urlpatterns = [
    path("profile/create/", create_parent, name="parent_create"),
    path("profile/update/", change_password_parent, name="parent_update"),
    path("profile/email/", change_email_parent, name="parent_email"),
    path("profile/delete/", delete_parent, name="parent_delete"),
]
