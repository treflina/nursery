from autocomplete import HTMXAutoComplete
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("", include("apps.core.urls")),
    path("", include("apps.info.urls")),
    path("", include("apps.kids.urls")),
    path("", include("apps.absences.urls")),
    path("", include("apps.billings.urls")),
    path("", include("apps.users.urls")),
    path("konto/", include("django.contrib.auth.urls")),
    path("webpush/", include("webpush.urls")),
    path(
        "manifest.json",
        TemplateView.as_view(
            template_name="manifest.json", content_type="application/json"
        ),
        name="manifest.json",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    *HTMXAutoComplete.url_dispatcher("ac"),
]

if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
