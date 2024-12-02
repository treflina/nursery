from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django_htmx.http import trigger_client_event

from apps.core.filters import BaseFilter
from apps.core.utils.helpers import reverse_querystring
from apps.users.permissions import (
    check_employee,
    login_required_htmx,
)

from .forms import ContributionForm
from .models import Contribution, ContributionStatus


@login_required_htmx
def contributions(request, pk=None):
    contributions = Contribution.objects.all()
    if pk is None:
        contribution = contributions.last()
    else:
        contribution = contributions.filter(id=pk).last()

    contribution_list = []
    filter = None
    if contribution:
        contribution_list = (
            ContributionStatus.objects.filter(
                contribution=contribution, not_applicable=False
            )
            .select_related("child", "contribution")
            .order_by("paid", "child")
        )
        if contribution_list:
            filter = BaseFilter(request.GET, queryset=contribution_list)

    return render(
        request,
        "contributions/contributions.html",
        context={
            "contributions": contributions,
            "selected_contribution": contribution,
            "contribution_list": contribution_list,
            "filter": filter,
        },
    )


@login_required_htmx
@user_passes_test(check_employee)
def create_contribution(request):
    form = ContributionForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            msg = _("New contribution has been added.")
            trigger_client_event(resp, "contributionCreated")
            return trigger_client_event(resp, "showToast", {"msg": msg})

    return render(
        request, "contributions/contribution_form.html", {"form": form, "add": True}
    )


@login_required_htmx
@user_passes_test(check_employee)
def update_contribution(request, pk):
    obj = get_object_or_404(Contribution, pk=pk)
    form = ContributionForm(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            resp = HttpResponse(status=204)
            msg = _("Contribution has been updated.")
            trigger_client_event(resp, "contributionCreated")
            return trigger_client_event(resp, "showToast", {"msg": msg})

    return render(
        request, "contributions/contribution_form.html", {"form": form, "add": False}
    )


@login_required_htmx
@user_passes_test(check_employee)
def update_contribution_status(request, pk):
    if request.method == "POST" and request.htmx:
        if request.htmx.trigger_name == "paid":
            contribution_status = ContributionStatus.objects.filter(id=pk).last()
            if contribution_status:
                contribution_status.paid = not contribution_status.paid
                contribution_status.save()
    query = request.POST.get("query", "")

    return HttpResponseRedirect(
        reverse_querystring(
            "contributions:contributions",
            query_kwargs={"query": query},
        )
    )


@login_required_htmx
@user_passes_test(check_employee)
def update_contribution_published(request, pk):
    if request.method == "POST":
        contribution = get_object_or_404(Contribution, pk=pk)
        contribution.published = not contribution.published
        contribution.save()
        if request.htmx:
            return HttpResponse(
                render(
                    request,
                    "contributions/includes/contribution_published.html",
                    {"selected_contribution": contribution},
                )
            )
    return HttpResponseRedirect(
        reverse("contributions:contributions", kwargs={"pk": contribution.id})
    )


@login_required_htmx
@user_passes_test(check_employee)
@require_http_methods(["DELETE"])
def delete_contribution(request, pk):
    if request.htmx:
        contribution_to_delete = get_object_or_404(Contribution, pk=pk)
        contribution_to_delete.delete()
        resp = HttpResponseRedirect(reverse("contributions:contributions"))
        msg = _("Contribution has been deleted.")
        return trigger_client_event(resp, "showToast", {"msg": msg})
