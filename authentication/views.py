from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import PersonalUserCreationForm

class UserSignUpView(generic.CreateView):
    """ signup view """
    form_class = PersonalUserCreationForm
    success_url = reverse_lazy('trocgraines:homepage')
    template_name = 'signup.html'

    def form_valid(self, form):
        """ log in automatically after sign up and add confirmation message"""
        valid = super().form_valid(form)
        login(self.request, self.object)
        messages.success(
            self.request,
            'Heureux de vous connaître ' + self.request.user.username
        )
        return valid

class UserLoginView(LoginView):
    """ overload LoginView to add confirmation message """
    def form_valid(self, form):
        """ add login succes messages """
        valid = super().form_valid(form)
        messages.success(
            self.request,
            'Content de vous revoir ' + self.request.user.username
        )
        return valid

class UserLogoutView(LogoutView):
    """ overload LogoutView to add confirmation message """

    def dispatch(self, request, *args, **kwargs):
        """ add logout confirm messages """
        messages.success(
            request,
            'Vous etes déconnecté, au revoir ' + request.user.username
        )
        return super().dispatch(request, *args, **kwargs)
