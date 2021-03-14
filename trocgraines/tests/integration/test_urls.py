from django.test import SimpleTestCase
from django.urls import resolve, reverse

from trocgraines.views import homepage


class TestAppUsersUrls(SimpleTestCase):
    def test_homepage_url_resolves(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)
