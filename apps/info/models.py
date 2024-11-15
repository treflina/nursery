from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeUserStampedModel
from apps.kids.models import Child


class Menu(models.Model):

    menu_date = models.DateField(_("Date"))
    breakfast = models.TextField(_("Breakfast"), null=True, blank=True)
    soup = models.TextField(_("Soup"), null=True, blank=True)
    lunch = models.TextField(_("Lunch"), null=True, blank=True)
    teatime = models.TextField(_("Teatime"), null=True, blank=True)

    def __str__(self):
        return f"Menu {self.menu_date}"


class Note(models.Model):

    note_date = models.DateField(_("Date"))
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    content = models.TextField(_("Content"))

    def __str__(self):
        return f"Note {self.note_date}: {self.child}"


class MainTopic(TimeUserStampedModel):
    description = models.CharField(_("Description"), max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Main Topic")
        verbose_name_plural = _("Main Topics")
        ordering = ["-created_at"]


class Activities(models.Model):

    day = models.DateField(_("Date"))
    main_topic = models.ForeignKey(
        "info.MainTopic", on_delete=models.PROTECT, blank=True, null=True
    )
    topic = models.CharField(_("Topic"), max_length=255, blank=True, null=True)
    activity = models.TextField(_("Kids activity"), blank=True, null=True)
    movement = models.TextField(_("Motor activity"), blank=True, null=True)
    music = models.TextField(_("Musical activity"), blank=True, null=True)
    art = models.TextField(_("Art activity"), blank=True, null=True)
    other = models.TextField(_("Inne"), blank=True, null=True)

    def __str__(self):
        return f"Activities {self.day}"


# class ActivityType(models.Model):

#     name = models.CharField(_("Activity Type"), max_length=50)
#     order = models.SmallIntegerField(_("Order"), default=0)

#     def __str__(self):
#         return self.name


# class Activity(models.Model):

#     activity_date = models.DateField(_("Activity date"))
#     activity_type = models.ForeignKey(
#         ActivityType,
#         verbose_name=_("Activity Type"),
#         on_delete=models.CASCADE
#         )
#     description = models.TextField(_("Description"))


# class MainTopic(models.Model):
#     date_from = models.DateField(_("Date from"))
#     date_to = models.DateField(_("Date to"))
#     name = models.CharField(_("Main Topic"))


# class DailyTopic(models.Model):
#     date = models.DateField()
