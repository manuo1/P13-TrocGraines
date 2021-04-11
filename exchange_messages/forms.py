from django import forms

from .models import ExchangeMessage
from .text_constants import NEW_MESSAGE_LABEL


class NewMessageForm(forms.ModelForm):

    """ form used for the exchange messages """

    class Meta:
        model = ExchangeMessage
        fields = ['message']
        labels = {'message': NEW_MESSAGE_LABEL}
