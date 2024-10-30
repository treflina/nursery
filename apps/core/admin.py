from django.contrib import admin

from .models import AdditionalDayOff, FoodPrice

admin.site.register(FoodPrice)
admin.site.register(AdditionalDayOff)
