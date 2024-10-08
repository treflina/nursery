from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import Parent


class Child(models.Model):

    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    birth_date = models.DateField(_("Date of birth"), blank=True, null=True)
    admission_date = models.DateField(_("Admission date"), default=date.today)
    leave_date = models.DateField(_("Leave date"), blank=True, null=True)
    parent = models.ForeignKey(Parent, blank=True, null=True, on_delete=models.PROTECT)
    food_price = models.ForeignKey(
        "core.FoodPrice", on_delete=models.PROTECT, blank=True, null=True
    )
    local_subsidy = models.BooleanField(_("Local subsidy"), default=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = _("Child")
        verbose_name_plural = _("Children")
        ordering = ("last_name", "first_name", "id")
