from django.shortcuts import render


def resp_err(request, template, form):
    """Error response with additional htmx headers."""

    resp = render(request, template, {"form": form})
    resp["HX-Retarget"] = "#absence-errors"
    resp["HX-Reselect"] = "#absence-errors"
    return resp
