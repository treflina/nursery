from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView
from django_htmx.http import trigger_client_event

from .forms import (
    GetParentForm,
    ParentChangeEmailForm,
    ParentChangePasswordForm,
    ParentForm,
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
            resp = HttpResponse(status=204)
            msg = _("User's account has been created.")
            return trigger_client_event(resp, "showToast", {"msg": msg})
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
            # messages.success(request, )
            resp = HttpResponse(status=204)
            msg = _("User's password has been changed.")
            return trigger_client_event(resp, "showToast", {"msg": msg})
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
            resp = HttpResponse(status=204)
            msg = _("User's email has been changed.")
            return trigger_client_event(resp, "showToast", {"msg": msg})
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
            resp = HttpResponse(status=204)
            msg = _("User's account has been deleted.")
            return trigger_client_event(resp, "showToast", {"msg": msg})

    else:
        form = GetParentForm()
    return render(request, "users/parent_form.html", {"form2": form, "delete": True})
