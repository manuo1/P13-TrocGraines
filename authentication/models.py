from django.contrib.auth.models import AbstractUser
from django.db import Error, IntegrityError, models
from django.shortcuts import get_object_or_404

from .text_constants import (EMAIL_CHANGE_CONFIRM_MSG,
                             EMAIL_CHANGE_UNIQ_ERROR_MSG, GLOBAL_ERROR_MSG,
                             USERNAME_CHANGE_CONFIRM_MSG,
                             USERNAME_CHANGE_UNIQ_ERROR_MSG)


class User(AbstractUser):
    """ custom user model """

    ranking = models.SmallIntegerField(default=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class UsersManager(models.Manager):
    """addition of a manager to the User class."""

    def update_user_data(self, user, new_data):
        """ update user's personal information """

        messages = []
        previous_user_data = {'username': user.username, 'email': user.email}
        """ try to change the username if it is different """
        if user.username != new_data['username']:
            user.username = new_data['username']
            try:
                user.save()
                messages.append({25: USERNAME_CHANGE_CONFIRM_MSG})
            except IntegrityError:
                user.username = previous_user_data['username']
                messages.append({40: USERNAME_CHANGE_UNIQ_ERROR_MSG})
            except Error:
                user.username = previous_user_data['username']
                messages.append({40: GLOBAL_ERROR_MSG})
        """ try to change the email if it is different """
        if user.email != new_data['email']:
            user.email = new_data['email']
            try:
                user.save()
                messages.append({25: EMAIL_CHANGE_CONFIRM_MSG})
            except IntegrityError:
                user.email = previous_user_data['email']
                messages.append({40: EMAIL_CHANGE_UNIQ_ERROR_MSG})
            except Error:
                user.email = previous_user_data['email']
                messages.append({40: GLOBAL_ERROR_MSG})

        return messages

    def get_user(slef, user_id):
        """ return user from is id """
        user = get_object_or_404(User, pk=user_id)
        return user
