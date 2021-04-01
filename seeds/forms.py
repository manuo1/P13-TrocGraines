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
                attrs={'placeholder': 'Ex : Pomme de terre Bintje (100 caractères maximum)'}
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Ex : Très jolie pomme de terre de ma production (300 caractères maximum)',
                    'maxlength': '300',
                }
            ),
        }



class SeedSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100
    )

    def __init__(self, *args, **kwargs):
        super(SeedSearchForm, self).__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({
            'class': 'form-control col-lg-9 col-sm-12',
            'placeholder': 'Chercher une graine',
            'aria-label': 'Search'
        })
