from django.urls import path, register_converter

from apps.core.converters import DateConverter

from .views import (
    BillingsReportsView,
    BillingUpdateView,
    billing,
    billing_confirm,
    billing_paid_update,
    billing_response_updateview,
    billing_update_notes,
    delete_billing,
    delete_billings,
    export_xlsx_file,
    generate_report,
    send_billing,
)

register_converter(DateConverter, "date")

app_name = "billings"

urlpatterns = [
    path("generuj-raport/", generate_report, name="create"),
    path("rachunek/<date:chosendate>/", billing, name="billing"),
    path(
        "rachunki/edytuj/zaplacone/<int:pk>/", billing_paid_update, name="paid_update"
    ),
    path(
        "rachunek/edytuj/<int:pk>/",
        BillingUpdateView.as_view(),
        name="billing_update",
    ),
    path(
        "rachunek/zatwierdz/<int:pk>/",
        billing_confirm,
        name="confirm",
    ),
    path("export_xlsx/<int:year>/<int:month>/", export_xlsx_file, name="export_file"),
    path("export_xlsx/", export_xlsx_file, name="export_file"),
    path(
        "rachunki/edytuj/",
        billing_response_updateview,
        name="billings_update",
    ),
    path(
        "rachunek/wyslij_email/<int:pk>/",
        send_billing,
        name="email",
    ),
    path(
        "rachunek/notatki/<int:pk>/",
        billing_update_notes,
        name="update_notes",
    ),
    path("rachunek/usun/<int:pk>/", delete_billing, name="delete"),
    path("rachunki/usun/", delete_billings, name="delete_selection"),
    path(
        "rachunki/",
        BillingsReportsView.as_view(),
        name="billings",
    ),
]
