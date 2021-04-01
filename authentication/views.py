from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import PersonalUserCreationForm, UserInformationUpdateForm
from .models import UsersManager

user_manager = UsersManager()

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
            'Bienvenu sur Troc Graine {}, heureux de vous connaître'.format(
                self.request.user.username
            )
        )
        return valid

class UserLoginView(LoginView):
    """ overload LoginView to add confirmation message """
    def form_valid(self, form):
        """ add login succes messages """
        valid = super().form_valid(form)
        messages.success(
            self.request,
            'Content de vous revoir {}'.format(self.request.user.username)
        )
        return valid

class UserLogoutView(LogoutView):
    """ overload LogoutView to add confirmation message """

    def dispatch(self, request, *args, **kwargs):
        """ add logout confirm messages """
        messages.success(
            request,
            'Vous êtes déconnecté(e), au revoir {}'.format(request.user.username)
        )
        return super().dispatch(request, *args, **kwargs)

class PersonalPasswordChangeView(PasswordChangeView):
    """Add a message to confirm that the password change worked."""


    def form_valid(self, form):
        messages.success(self.request, 'Votre mot de passe a été modifié')
        return super().form_valid(form)


@login_required()
def personalInformations(request):

    user_update_form = UserInformationUpdateForm(
        initial={
            'username_update': request.user.username,
            'email_update': request.user.email,})

    if request.method == 'POST':
        template = 'personal_informations_update.html'
    else:
        template = 'personal_informations.html'
        user_update_form.fields['username_update'].disabled = True
        user_update_form.fields['email_update'].disabled = True

    context={ 'user_update_form': user_update_form }
    return render(request, template, context)


@login_required()
def personalInformationsUpdate(request):

    user_update_form = UserInformationUpdateForm(
        initial={
            'username_update': request.user.username,
            'email_update': request.user.email,})

    if request.method == 'POST':
        completed_form = UserInformationUpdateForm(request.POST)
        if completed_form.is_valid():
            """ get new user data from form """
            new_user_data = {
                'username': completed_form.cleaned_data.get('username_update'),
                'email': completed_form.cleaned_data.get('email_update')
            }
            messages_from_user_manager = user_manager.update_user_data(
                    request.user, new_user_data
            )
            if messages_from_user_manager:
                for message in messages_from_user_manager:
                    for level, content in message.items():
                        messages.add_message(request, level, content)
        user_update_form = UserInformationUpdateForm(
            initial={
                'username_update': request.user.username,
                'email_update': request.user.email,})

        template = 'personal_informations.html'
        user_update_form.fields['username_update'].disabled = True
        user_update_form.fields['email_update'].disabled = True

    else:
        template = 'personal_informations_update.html'

    context={ 'user_update_form': user_update_form }
    return render(request, template, context)
