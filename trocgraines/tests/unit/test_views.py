from unittest import mock

from django.test import RequestFactory, TestCase

from trocgraines.views import homepage


class ViewsUnitTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_homepage(self):
        request = self.factory.get('/')
        response = homepage(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="seed_search_form"', str(response.content))
