from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import User


def check_employee(u):
    if u.is_anonymous:
        return False
    if u.is_superuser:
        return True
    if u.type == User.Types.EMPLOYEE and u.is_active:
        return True
    return False


def check_parent(u):
    if u.is_anonymous:
        return False
    if u.is_superuser:
        return True
    if u.type == User.Types.PARENT and u.is_active:
        return True
    return False


def check_accountant(u):
    if u.is_anonymous:
        return False
    if u.is_superuser:
        return True
    if u.type == User.Types.ACOUNTANT and u.is_active:
        return True
    return False


def check_staff(u):
    if u.is_anonymous:
        return False
    if u.is_superuser:
        return True
    if (
        (u.type == User.Types.ACOUNTANT or u.type == User.Types.EMPLOYEE)
        and u.is_active
    ):
        return True
    return False


class EmployeePermissionMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not check_employee(request.user):
            return HttpResponseRedirect(reverse("login"))

        return super().dispatch(request, *args, **kwargs)


class StaffPermissionMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not check_staff(request.user):
            return HttpResponseRedirect(reverse("login"))

        return super().dispatch(request, *args, **kwargs)
