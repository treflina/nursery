from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeUserStampedModel
from apps.kids.models import Child

from .managers import AbsenceManager


class Absence(TimeUserStampedModel):

    class TYPE_CHOICES(models.TextChoices):
        REP = "R", _("reported")
        NOT_REP = "NR", _("not reported")
        FIRST_REP = "FR", _("first day")
        OTHER = "O", _("other")

    child = models.ForeignKey(Child, verbose_name=_("Child"), on_delete=models.CASCADE)
    a_date = models.DateField(_("Date"))
    absence_type = models.CharField(
        _("Type of absence"), choices=TYPE_CHOICES, default="NR", max_length=20
    )

    reason = models.TextField(_("Reason"), null=True, blank=True)

    objects = AbsenceManager()

    class Meta:
        verbose_name = _("Absence")
        verbose_name_plural = _("Absences")

    def __str__(self):
        return f"Absence {self.child} - {self.a_date}"
