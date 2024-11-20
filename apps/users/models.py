from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    class Types(models.TextChoices):
        EMPLOYEE = "EMPLOYEE", "Employee"
        PARENT = "PARENT", "Parent"
        ACOUNTANT = "ACCOUNTANT", "Accountant"

    base_type = Types.PARENT

    type = models.CharField(
        _("Type"), max_length=20, choices=Types.choices, default=Types.PARENT
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.base_type
        return super().save(*args, **kwargs)


class ParentManager(BaseUserManager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=User.Types.PARENT)


class Parent(User):

    base_type = User.Types.PARENT

    objects = ParentManager()

    class Meta:
        proxy = True

    def __str__(self):
        if self.email != "":
            return f"{self.username} ({self.email})"
        return self.username


class EmployeeManager(BaseUserManager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=User.Types.EMPLOYEE)


class Employee(User):

    base_type = User.Types.EMPLOYEE

    objects = EmployeeManager()

    class Meta:
        proxy = True


class AccountantManager(BaseUserManager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=User.Types.EMPLOYEE)


class Accountant(User):

    base_type = User.Types.ACOUNTANT

    objects = AccountantManager()

    class Meta:
        proxy = True
