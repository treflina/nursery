from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import ParentForm
from .models import Parent


class ParentUpdate(UpdateView):

    model = Parent
    template_name = "users/parent_create.html"
    form_class = ParentForm
    success_url = reverse_lazy("kids:children")


class ParentCreate(CreateView):

    model = Parent
    template_name = "users/parent_create.html"
    form_class = ParentForm
    success_url = reverse_lazy("kids:children")
