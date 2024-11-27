from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse

from .models import User


def login_required_htmx(
    function=None, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME
):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated and request.htmx:
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            return HttpResponse(status=204, headers={"HX-Redirect": resolved_login_url})
        return login_required(
            function=function,
            login_url=login_url,
            redirect_field_name=redirect_field_name,
        )(request, *args, **kwargs)

    return wrapper


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
        u.type == User.Types.ACOUNTANT or u.type == User.Types.EMPLOYEE
    ) and u.is_active:
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
