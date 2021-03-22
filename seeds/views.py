from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import SeedCreateForm
from .models import Seed

class CreateSeedView(LoginRequiredMixin, CreateView):
    model = Seed
    form_class = SeedCreateForm
    template_name = 'add_seed.html'
    success_url = reverse_lazy('trocgraines:homepage')

    def form_valid(self, form):
        """ Add current user for SeedForm """
        form.instance.owner = self.request.user
        return super().form_valid(form)
