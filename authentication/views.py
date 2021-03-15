from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import PersonalUserCreationForm

class SignUpView(generic.CreateView):
    form_class = PersonalUserCreationForm
    success_url = '/auth/login/'
    template_name = 'signup.html'
