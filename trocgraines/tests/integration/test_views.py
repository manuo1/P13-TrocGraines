import os
from trocgraines_config.settings.common import BASE_DIR
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from django.urls import reverse

from seeds.models import Seed

class TestTrocgrainesViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.test_user_1 = self.User.objects.create_user(
            username='test_name',
            email='test_mail@mail.com',
            password='test_password',
        )

        self.log_form = {'username': 'test_name', 'password': 'test_password'}

        self.image_path = os.path.join(
            BASE_DIR,
            "static/assets/img/image_test.png"
        )
        self.test_seed_data = {
            'name': 'test seed name 2',
            'description': 'test seed description 2',
            'photo': 'img_data',
        }


    """ homepage view Tests """

    def test_if_homepage_view_return_homepage_template(self):
        response = self.client.get(reverse('trocgraines:homepage'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_homepage_get_return_last_seeds_added(self):
        seed_1 = self.create_a_seed('name_1')
        seed_2 = self.create_a_seed('name_2')
        response = self.client.get(reverse('trocgraines:homepage'))
        self.assertTrue (
            seed_1 in response.context['page_obj']
            and seed_2 in response.context['page_obj']
        )

    def test_homepage_post_return_searched_seed_matching_list(self):
        seed_x = self.create_a_seed('name_x')
        seed_y = self.create_a_seed('name_y')
        response = self.client.post(reverse('trocgraines:homepage'), {'search': 'name_x'})
        self.assertTrue (
            seed_x in response.context['page_obj']
            and seed_x.name in response.context['searched_seed']
            and seed_y not in response.context['page_obj']
        )




    def create_a_seed(self, name='name'):
        self.client.login(**self.log_form)
        with open(self.image_path, 'rb') as img_data:
            self.test_seed_data['photo'] = img_data
            self.test_seed_data['name'] = name
            self.client.post( reverse('seeds:add_seed'), self.test_seed_data )
        new_seed = get_object_or_404( Seed, name=self.test_seed_data['name'] )
        return new_seed
