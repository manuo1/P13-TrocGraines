from unittest import mock
from django.db.utils import IntegrityError, Error
from django.test import RequestFactory, TestCase

from seeds.models import SeedManager

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

        self.test_seed = MockSeed()
        self.test_seed_e = MockSeed_Error()

        self.seed_manager = SeedManager()


    def test_get_last_seeds_added(self):
        pass
