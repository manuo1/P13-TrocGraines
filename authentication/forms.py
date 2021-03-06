from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class PersonalUserCreationForm(UserCreationForm):
    """ custom parameters of the user account creation form """

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Visible par les autres utilisateurs'}
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': (
                        'Ne sera PAS visible par les autres utilisateurs')
                }
            ),
        }


class UserInformationUpdateForm(forms.Form):
    """ form used to modify the user's personal information """
    
    username_update = forms.CharField(
        initial="", max_length=100, label='Nom d\'utilisateur', disabled=False
    )
    email_update = forms.EmailField(
        initial="", max_length=100, label='Email', disabled=False
    )
