from django.db import models

from authentication.models import User

class Discussion(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
	       return self.recipient

class ExchangeMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    sending_date = models.DateTimeField(auto_now_add=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)

    def __str__(self):
	       return self.subject
