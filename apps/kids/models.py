from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import GovernmentSubsidy, LocalSubsidy, OtherSubsidy
from apps.users.models import Parent


class Child(models.Model):

    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    birth_date = models.DateField(_("Date of birth"), blank=True, null=True)
    admission_date = models.DateField(_("Admission date"), default=date.today)
    leave_date = models.DateField(_("Leave date"), blank=True, null=True)
    parent = models.ForeignKey(Parent, blank=True, null=True, on_delete=models.SET_NULL)
    food_price = models.ForeignKey(
        "core.FoodPrice", on_delete=models.PROTECT, blank=True, null=True
    )
    local_subsidy = models.BooleanField(_("Subsidy"), default=True)
    other_subsidies = models.ManyToManyField(
        OtherSubsidy, verbose_name=_("Other subsidies"), blank=True, null=True
    )
    gov_subsidy = models.ForeignKey(
        GovernmentSubsidy,
        verbose_name=_("Government subsidy"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def other_subsidies_sum(self):
        return sum([x.amount for x in self.other_subsidies.all()])

    @property
    def all_subsidies_sum(self):

        local_subsidy = LocalSubsidy.objects.last()
        if not local_subsidy:
            local = 0
        else:
            local = local_subsidy.amount

        gov_subsidy = self.gov_subsidy
        if not gov_subsidy:
            gov = 0
        else:
            gov = gov_subsidy.amount

        return sum([x.amount for x in self.other_subsidies.all()]) + local + gov

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = _("Child")
        verbose_name_plural = _("Children")
        ordering = ("last_name", "first_name", "id")
