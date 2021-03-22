from django import forms
from .models import Seed

class SeedCreateForm(forms.ModelForm):

    class Meta:
        model = Seed
        fields = ['name', 'description', 'photo']

class SeedSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        label='Recherche',
        widget=forms.TextInput(attrs={'placeholder': 'Chercher une graine'})
    )
