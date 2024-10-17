from autocomplete import HTMXAutoComplete
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("apps.core.urls")),
    path("", include("apps.info.urls")),
    path("", include("apps.kids.urls")),
    path("", include("apps.absences.urls")),
    path("", include("apps.billings.urls")),
    path("konto/", include("django.contrib.auth.urls")),
    *HTMXAutoComplete.url_dispatcher('ac'),
]

if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
