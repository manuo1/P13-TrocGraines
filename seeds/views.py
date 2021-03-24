from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import SeedCreateForm
from .models import Seed, SeedManager

seed_manager = SeedManager()

class CreateSeedView(LoginRequiredMixin, CreateView):
    model = Seed
    form_class = SeedCreateForm
    template_name = 'add_seed.html'
    success_url = reverse_lazy('trocgraines:homepage')

    def form_valid(self, form):
        """ Add current user for SeedCreateForm """
        form.instance.owner = self.request.user
        return super().form_valid(form)

@login_required()
def my_seeds(request):

    if request.method == 'POST':
        try:
            seed_id = request.POST.get('seed_availability')
            seed_manager.changes_seed_availability(seed_id)
        except Http404:
            pass



    matching_list = seed_manager.get_user_seeds(request.user)
    context={ 'matching_list': matching_list, }
    return render(request, 'my_seeds.html', context)
