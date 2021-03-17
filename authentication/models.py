from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    account_creation_date = models.DateTimeField(auto_now_add=True)
    ranking = models.SmallIntegerField(default=100)
