from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeUserStampedModel
from apps.kids.models import Child


class Billing(TimeUserStampedModel):

    date_month = models.DateField(_("Month"))
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    food_price = models.DecimalField(
        _("Food price"), max_digits=4, decimal_places=2, default=0
    )
    food_total = models.DecimalField(
        _("Food total"), max_digits=5, decimal_places=2, default=0
    )
    monthly_payment = models.DecimalField(
        _("Monthly payment"), max_digits=6, decimal_places=2, default=0
    )
    days_count = models.PositiveIntegerField(_("Payable days count"), default=0)
    zus_transfer = models.BooleanField(_("ZUS"), default=False)
    paid = models.BooleanField(_("Paid"), default=False)

    def __str__(self):
        return f"{self.date_month.strftime("%m-%Y")}: {self.child}"
