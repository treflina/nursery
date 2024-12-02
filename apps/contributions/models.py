from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from apps.kids.models import Child

from . import signals


class Contribution(models.Model):

    name = models.CharField(_("Name"), max_length=255)
    name_full = models.CharField(_("Name for parents"), max_length=255, default="")
    amount = models.DecimalField(_("Amount"), default=0, max_digits=5, decimal_places=2)
    published = models.BooleanField(_("Published"), default=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Contribution")
        verbose_name_plural = _("Contributions")


class ContributionStatus(models.Model):

    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    not_applicable = models.BooleanField(default=False)

    def __str__(self):
        paid = _("Yes") if self.paid is True else _("No")
        return f"{self.contribution} - {self.child.full_name} - {paid}"

    class Meta:
        verbose_name = _("Contribution status")
        verbose_name_plural = _("Contribution statuses")


post_save.connect(
    signals.create_new_contributionstatus_if_new_contribution, sender=Contribution
)
