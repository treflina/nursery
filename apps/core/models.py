from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeUserStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("changed by"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class AdditionalDayOff(models.Model):

    day = models.DateField()

    def __str__(self):
        return f"{self.day}"

    class Meta:
        verbose_name = _("Additional day off")
        verbose_name_plural = _("Additional days off")
        ordering = ("day",)


class FoodPrice(models.Model):

    name = models.CharField(_("Name"), max_length=255, null=False, blank=False)
    price = models.DecimalField(_("Price"), max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}: {self.price} zł"


class MonthlyPayment(models.Model):

    price = models.DecimalField(_("Amount"), max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.price} zł"


class LocalSubsidy(models.Model):

    amount = models.DecimalField(_("Amount"), max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"Local subsidy {self.amount} zł"

    class Meta:
        verbose_name = _("Local subsidy")
        verbose_name_plural = _("Local subsidies")


class GovernmentSubsidy(models.Model):

    name = models.CharField(_("Name"), max_length=255)
    amount = models.DecimalField(_("Amount"), max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}: {self.amount} zł"

    class Meta:
        verbose_name = _("Government subsidy")
        verbose_name_plural = _("Government subsidies")


class OtherSubsidy(models.Model):

    name = models.CharField(_("Name"), max_length=255)
    amount = models.DecimalField(_("Amount"), max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}: {self.amount} zł"

    class Meta:
        verbose_name = _("Other subsidy")
        verbose_name_plural = _("Other subsidies")
