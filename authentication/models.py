from django.contrib.auth.models import AbstractUser
from django.db import IntegrityError, Error, models


class User(AbstractUser):
    ranking = models.SmallIntegerField(default=100)

class UsersManager(models.Manager):
    """addition of a manager to the User class."""

    def update_user_data(self, user, new_data):
        messages = []
        previous_user_data = {
            'username': user.username,
            'email': user.email
        }
        """ try to change the username if it is different """
        if user.username != new_data['username']:
            user.username = new_data['username']
            try:
                user.save()
                messages.append({25: 'Votre nom d’utilisateur a été modifié'})
            except IntegrityError:
                user.username = previous_user_data['username']
                messages.append({40: 'Ce nom d\'utilisateur est déja utilisé'})
            except Error:
                user.username = previous_user_data['username']
                messages.append({40: 'Une erreur est survenue'})
        """ try to change the email if it is different """
        if user.email != new_data['email']:
            user.email = new_data['email']
            try:
                user.save()
                messages.append({25: 'Votre email a été modifié'})
            except Error:
                user.email = previous_user_data['email']
                messages.append({40: 'Une erreur est survenue'})

        return messages
