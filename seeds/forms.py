from django import forms
from .models import Seed

class SeedCreateForm(forms.ModelForm):

    class Meta:
        model = Seed
        fields = ['name', 'description', 'photo']
        labels = {
            'name': 'Nom de votre graine',
            'description': 'Description',
            'photo': 'Ajoutez une photo du plus beau sourire de votre graine',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Ex : Graine de tomate'}
            ),
            'description': forms.Textarea(
                attrs={'placeholder': 'Ex : Très jolie tomate de ma production'}
            ),
        }


class SeedSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        label='Recherche',
        widget=forms.TextInput(attrs={'placeholder': 'Chercher une graine'})
    )
