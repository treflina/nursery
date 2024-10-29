from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import (
    GetParentForm,
    ParentForm,
    ParentChangePasswordForm,
    ParentChangeEmailForm,
)
from .models import Parent


class ParentUpdate(UpdateView):

    model = Parent
    template_name = "users/parent_form.html"
    form_class = ParentForm
    success_url = reverse_lazy("kids:children")


def create_parent(request):
    if request.method == "POST":
        form = ParentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204)
    else:
        form = ParentForm()

    return render(request, "users/parent_form.html", {"form2": form, "add": True})


def change_password_parent(request):
    if request.method == "POST":
        form = ParentChangePasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            parent = Parent.objects.filter(username=username).last()
            parent.set_password(form.cleaned_data["password"])
            parent.save()
            messages.success(request, _("User's password has been changed."))
            return HttpResponse(status=204, headers={"HX-Trigger": "passwordChanged"})
    else:
        form = ParentChangePasswordForm()

    return render(request, "users/parent_form.html", {"form2": form, "update": True})


def change_email_parent(request):
    if request.method == "POST":
        form = ParentChangeEmailForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            Parent.objects.filter(username=username).update(email=email)
            messages.success(request, _("User's email has been changed."))
            return HttpResponse(status=204)
    else:
        form = ParentChangeEmailForm()

    return render(
        request, "users/parent_form.html", {"form2": form, "change_email": True}
    )


def delete_parent(request):
    if request.method == "POST":
        form = GetParentForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            Parent.objects.filter(username=username).delete()
            messages.success(request, _("User's account has been deleted."))
            return HttpResponse(status=204)
    else:
        form = GetParentForm()
    return render(request, "users/parent_form.html", {"form2": form, "delete": True})
