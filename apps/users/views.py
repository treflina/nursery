from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import GetParentForm, ParentForm, ParentUpdateForm
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


def update_parent(request):
    if request.method == "POST":
        form = ParentUpdateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            parent = Parent.objects.filter(username=username).last()
            parent.set_password(form.cleaned_data["password"])
            parent.save()
            return HttpResponse(status=204)
    else:
        form = ParentUpdateForm()

    return render(request, "users/parent_form.html", {"form2": form, "update": True})


def delete_parent(request):
    if request.method == "POST":
        form = GetParentForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            Parent.objects.filter(username=username).delete()
            return HttpResponse(status=204)
    else:
        form = GetParentForm()
    return render(request, "users/parent_form.html", {"form2": form, "delete": True})
