from django.urls import path, register_converter

from apps.core.converters import DateConverter

from .views import (BillingListView, BillingsReportsView, billing,
                    billing_response_updateview, generate_report)

register_converter(DateConverter, "date")

app_name = "billings"

urlpatterns = [
    path("report/<int:year>/<int:month>/", BillingListView.as_view(), name="report"),
    path("report/", BillingListView.as_view(), name="report"),
    path("generate-report/", generate_report, name="generate_report"),
    path("billing/<date:chosendate>/", billing, name="billing"),
    path(
        "billings/",
        BillingsReportsView.as_view(),
        name="billings",
    ),
    path(
        "billings/update/",
        billing_response_updateview,
        name="billings_update",
    ),
]
