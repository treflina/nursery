from django.contrib import admin

from .models import Contribution, ContributionStatus

admin.site.register(Contribution)
admin.site.register(ContributionStatus)
