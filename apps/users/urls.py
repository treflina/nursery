from django.urls import path

from .views import ParentCreate, ParentUpdate

app_name = "users"

urlpatterns = [
    path("profile/update/<int:pk>/", ParentUpdate.as_view(), name="parent_update"),
    path("profile/create/", ParentCreate.as_view(), name="parent_create"),
]
