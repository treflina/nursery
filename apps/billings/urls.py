from django.urls import path, register_converter

from apps.core.converters import DateConverter

from .views import (BillingListView, BillingsReportsView, BillingUpdateView,
                    billing, billing_confirm, billing_paid_update,
                    billing_response_updateview, billing_update_notes,
                    delete_billing, delete_billings, export_xlsx_file,
                    generate_report, send_billing)

register_converter(DateConverter, "date")

app_name = "billings"

urlpatterns = [
    path("report/<int:year>/<int:month>/", BillingListView.as_view(), name="report"),
    path("report/", BillingListView.as_view(), name="report"),
    path("generate-report/", generate_report, name="generate_report"),
    path("billing/<date:chosendate>/", billing, name="billing"),
    path("billings/update/paid/<int:pk>/", billing_paid_update, name="paid_update"),
    path(
        "billing/update/<int:pk>/",
        BillingUpdateView.as_view(),
        name="billing_update",
    ),
    path(
        "billing/confirm/<int:pk>/",
        billing_confirm,
        name="confirm",
    ),
    path("export_xlsx/<int:year>/<int:month>/", export_xlsx_file, name="export_file"),
    path("export_xlsx/", export_xlsx_file, name="export_file"),
    path(
        "billings/update/",
        billing_response_updateview,
        name="billings_update",
    ),
    path(
        "billing/send_email/<int:pk>/",
        send_billing,
        name="email",
    ),
    path(
        "billings/update_notes/<int:pk>/",
        billing_update_notes,
        name="update_notes",
    ),
    path("billing/delete/<int:pk>/", delete_billing, name="delete"),
    path("billings/delete/", delete_billings, name="delete_selection"),
    path(
        "billings/",
        BillingsReportsView.as_view(),
        name="billings",
    ),
]
