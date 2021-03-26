import os
from trocgraines_config.settings.common import BASE_DIR
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from django.urls import reverse

from imagekit.models import ProcessedImageField

from seeds.models import Seed

class TestSeedViews(TestCase):
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

    def test_user_can_add_a_seed(self):
        """ test if user can add a seed """
        number_of_seeds_before = Seed.objects.count()
        new_seed = self.create_a_seed()
        number_of_seeds_after = Seed.objects.count()
        self.assertTrue( new_seed is not None )
        self.assertTrue( number_of_seeds_after > number_of_seeds_before)

    def test_user_can_delette_a_seed(self):
        """ test if user can delette a seed """
        new_seed = self.create_a_seed()
        number_of_seeds_before = Seed.objects.count()
        self.client.post(
            reverse('seeds:my_seeds'),
            {'delete_seed': new_seed.id}
        )
        number_of_seeds_after = Seed.objects.count()
        self.assertTrue( number_of_seeds_after < number_of_seeds_before )

    def test_user_can_change_availability_of_a_seed(self):
        """ test if user can change availability of a seed """
        new_seed = self.create_a_seed()
        seed_availability_before = new_seed.available
        self.client.post(
            reverse('seeds:my_seeds'),
            {'seed_availability': new_seed.id}
        )
        modified_seed = get_object_or_404(Seed,pk=new_seed.id)
        seed_availability_after = modified_seed.available
        self.assertTrue( seed_availability_before != seed_availability_after )

    def test_my_seeds_view_request_post_without_names(self):
        """ test if my_seeds view post method without """
        """ arg return right template """
        self.client.login(**self.log_form)
        response = self.client.post(reverse('seeds:my_seeds'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_seeds.html')

    def create_a_seed(self):
        self.client.login(**self.log_form)
        with open(self.image_path, 'rb') as img_data:
            self.test_seed_data['photo'] = img_data
            self.client.post( reverse('seeds:add_seed'), self.test_seed_data )
        new_seed = get_object_or_404( Seed, name=self.test_seed_data['name'] )
        return new_seed
