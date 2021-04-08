from unittest import mock

from django.db.utils import Error
from django.test import TestCase

from seeds.models import SeedManager


class SeeModelsUnitTest(TestCase):
    def setUp(self):
        self.new_data = {'username': 'testusername2', 'email': 'testemail2'}

        class MockUser:
            def __init__(self):
                self.username = 'testusername'
                self.email = 'testemail'
                self.password = 'testpassword'

        self.test_user = MockUser()

        class MockSeed:
            def __init__(self):
                self.name = 'testusername'
                self.description = 'testemail'
                self.photo = 'testpassword'
                self.creation_date = 'date'
                self.available = True
                self.owner = MockUser()

            def save(self):
                pass

            def delete(self):
                pass

        class MockSeed_Error:
            def __init__(self):
                self.name = 'testusername'
                self.description = 'testemail'
                self.photo = 'testpassword'
                self.creation_date = 'date'
                self.available = True
                self.owner = MockUser()

            def save(self):
                raise Error

            def delete(self):
                raise Error

        self.test_seed = MockSeed()
        self.test_seed_e = MockSeed_Error()
        self.seed_manager = SeedManager()

    def test_changes_seed_availability_success(self):
        with mock.patch(
            'seeds.models.get_object_or_404',
            return_value=self.test_seed,
        ):

            messages = self.seed_manager.changes_seed_availability('1234')
            self.assertTrue(
                self.test_seed.available is False and messages == []
            )

    def test_changes_seed_availability_error(self):
        with mock.patch(
            'seeds.models.get_object_or_404',
            return_value=self.test_seed_e,
        ):

            messages = self.seed_manager.changes_seed_availability('1234')
            self.assertTrue(messages == [{40: 'Une erreur est survenue'}])

    def test_delete_seed_success(self):
        with mock.patch(
            'seeds.models.get_object_or_404',
            return_value=self.test_seed,
        ):

            messages = self.seed_manager.delete_seed('1234')
            self.assertTrue(
                messages
                == [
                    {
                        40: 'Vous venez de supprimer : {}'.format(
                            self.test_seed.name
                        )
                    }
                ]
            )

    def test_delete_seed_error(self):
        with mock.patch(
            'seeds.models.get_object_or_404',
            return_value=self.test_seed_e,
        ):

            messages = self.seed_manager.delete_seed('1234')
            self.assertTrue(messages == [{40: 'Une erreur est survenue'}])

    def test_get_seed(self):
        with mock.patch(
            'seeds.models.get_object_or_404',
            return_value=self.test_seed,
        ):

            seed = self.seed_manager.get_seed('1234')
            self.assertTrue(seed == self.test_seed)
