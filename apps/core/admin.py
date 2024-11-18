from django.contrib import admin

from .models import (
    AdditionalDayOff,
    FoodPrice,
    GovernmentSubsidy,
    LocalSubsidy,
    MonthlyPayment,
    OtherSubsidy,
)

admin.site.register(FoodPrice)
admin.site.register(AdditionalDayOff)
admin.site.register(MonthlyPayment)
admin.site.register(LocalSubsidy)
admin.site.register(GovernmentSubsidy)
admin.site.register(OtherSubsidy)
