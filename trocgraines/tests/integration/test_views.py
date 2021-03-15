from django.test import Client, TestCase
from django.urls import reverse

class TestTrocgrainesViews(TestCase):
    def setUp(self):
        self.client = Client()

    """ homepage view Tests """

    def test_if_homepage_view_return_homepage_template(self):
        response = self.client.get(reverse('trocgraines:homepage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
