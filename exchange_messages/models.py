from django.db import Error, models
from django.shortcuts import get_object_or_404

from authentication.models import User
from .text_constants import (
    GLOBAL_ERROR_MSG,
    DELETED_MSG
)

class ExchangeMessageManager(models.Manager):

    def save_exchange_message(self, **exchange_message_data):
        exchange_message = ExchangeMessage(
            recipient=exchange_message_data['recipient'],
            subject= exchange_message_data['subject'],
            message= exchange_message_data['message'],
        )
        discussion = Discussion(
            sender= exchange_message_data['sender'],
            exchange_message= exchange_message
        )
        try:
            exchange_message.save()
            discussion.save()
            return True
        except Error:
            return None

    def get_user_discussions(slef, user):
        discussions = []
        discussions = Discussion.objects.filter(sender=user).order_by(
            '-exchange_message')
        return discussions

    def delete_discussion(self, discussion_id):
        messages =''
        discussion = get_object_or_404(Discussion, pk=discussion_id)
        try:
            discussion.delete()
            messages = [{40: DELETED_MSG }]
        except Error:
            messages = [{40: GLOBAL_ERROR_MSG }]
        return messages




class ExchangeMessage(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    sending_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ret = str(self.sending_date) + self.subject
        return ret

class Discussion(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange_message = models.ForeignKey(
        ExchangeMessage,
        on_delete=models.CASCADE
    )

    def __str__(self):
        ret = (
            str(self.exchange_message.sending_date) + ' | id:' + str(self.id)
            + ' | ' + self.sender.username + ' -> '
            + self.exchange_message.recipient.username
        )
        return ret
