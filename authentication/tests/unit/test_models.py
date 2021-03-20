from unittest import mock
from django.db.utils import IntegrityError, Error
from django.test import RequestFactory, TestCase

from ...models import UsersManager

class ModelsUnitTest(TestCase):
    def setUp(self):
        self.new_data = {
            'username': 'testusername2',
            'email': 'testemail2'
        }

        class MockUser:
            def __init__(self):
                self.username = 'testusername'
                self.email = 'testemail'
                self.password = 'testpassword'
            def save(self):
                pass

        class MockUser_IntegrityError:
            def __init__(self):
                self.username = 'testusername'
                self.email = 'testemail'
                self.password = 'testpassword'
            def save(self):
                raise IntegrityError

        class MockUser_Error:
            def __init__(self):
                self.username = 'testusername'
                self.email = 'testemail'
                self.password = 'testpassword'
            def save(self):
                raise Error
        self.test_user = MockUser()
        self.test_user_ie = MockUser_IntegrityError()
        self.test_user_e = MockUser_Error()

        self.user_manager = UsersManager()

    def test_update_user_data_part_update_username(self):
        self.new_data['email'] = self.test_user.email
        messages = self.user_manager.update_user_data(
            self.test_user, self.new_data
        )
        self.assertIn(
            'Votre nom d’utilisateur a été modifié',
            messages[0].values()
        )

    def test_update_user_data_part_update_email(self):
        self.new_data['username'] = self.test_user.username
        messages = self.user_manager.update_user_data(
            self.test_user, self.new_data
        )
        self.assertIn(
            'Votre email a été modifié',
            messages[0].values()
        )

    def test_update_user_data_with_username_integrityerror_exception(self):
        self.new_data['email'] = self.test_user_ie.email
        messages = self.user_manager.update_user_data(
            self.test_user_ie, self.new_data
        )
        self.assertIn(
            'Ce nom d\'utilisateur est déja utilisé',
            messages[0].values()
        )

    def test_update_user_data_with_username_error_exception(self):
        self.new_data['email'] = self.test_user_e.email
        messages = self.user_manager.update_user_data(
            self.test_user_e, self.new_data
        )
        self.assertIn(
            'Une erreur est survenue',
            messages[0].values()
        )

    def test_update_user_data_with_email_error_exception(self):
        self.new_data['username'] = self.test_user_e.username
        messages = self.user_manager.update_user_data(
            self.test_user_e, self.new_data
        )
        self.assertIn(
            'Une erreur est survenue',
            messages[0].values()
        )
