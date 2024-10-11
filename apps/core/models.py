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


class FoodPrice(models.Model):

    name = models.CharField(_("Name"), max_length=255, null=False, blank=False)
    amount = models.DecimalField(_("Amount"), max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}: {self.amount} zł"
