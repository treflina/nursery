from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeUserStampedModel
from apps.kids.models import Child


class Billing(TimeUserStampedModel):

    TAG_CHOICES = [
        ("yellow", _("yellow")),
        ("green", _("green")),
    ]

    date_month = models.DateField(_("Month"))
    child = models.ForeignKey(Child, on_delete=models.SET_NULL, null=True)
    # TODO remove default
    child_name = models.CharField(_("Child's name"), max_length=255, default="")
    food_price = models.DecimalField(
        _("Food price"), max_digits=4, decimal_places=2, default=0
    )
    food_total = models.DecimalField(
        _("Food total"), max_digits=5, decimal_places=2, default=0
    )
    monthly_payment = models.DecimalField(
        _("Monthly payment"), max_digits=6, decimal_places=2, default=0
    )
    payment_to_charge = models.DecimalField(
        _("Payment to charge"), max_digits=6, decimal_places=2, default=0
    )
    days_count = models.PositiveIntegerField(_("Payable days count"), default=0)
    local_subsidy = models.DecimalField(
        _("Local subsidy"), max_digits=6, decimal_places=2, default=0
    )
    gov_subsidy = models.DecimalField(
        _("Government subsidy"), max_digits=6, decimal_places=2, default=0
    )
    other_subsidies = models.DecimalField(
        _("Other subsidies"), max_digits=6, decimal_places=2, default=0
    )
    sub_received = models.BooleanField(_("Subsidies received"), default=False)
    paid = models.BooleanField(_("Paid"), default=False)
    info_subsidies = models.TextField(
        _("Information about other subsidies"), null=True, blank=True
    )
    note = models.TextField(_("Note"), null=True, blank=True)
    info = models.TextField(_("Information for parents"), null=True, blank=True)
    tag = models.CharField(
        _("tag"), null=True, blank=True, choices=TAG_CHOICES, max_length=255
    )
    confirmed = models.BooleanField(_("Confirmed"), default=False)
    sent = models.BooleanField(_("Sent"), default=False)

    @property
    def payments_sum(self):
        return self.food_total + self.payment_to_charge

    @property
    def subsidies_sum(self):
        return self.local_subsidy + self.gov_subsidy + self.other_subsidies

    def __str__(self):
        return f"{self.date_month.strftime('%m-%Y')}: {self.child}"
