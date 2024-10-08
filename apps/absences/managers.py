from django.db import models


class AbsenceManager(models.Manager):

    def get_absence_child_month(self, child, year, month):
        qs = self.filter(
            child=child, a_date__month=month, a_date__year=year, absence_type="R"
        )
        return qs
