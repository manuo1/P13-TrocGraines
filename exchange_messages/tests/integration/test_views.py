import os

from django.contrib.auth import get_user_model
from django.core import mail
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from django.urls import reverse

from exchange_messages.models import Discussion
from seeds.models import Seed
from trocgraines_config.settings.common import BASE_DIR


class TestExchangeMessagesViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.test_seed_owner = self.User.objects.create_user(
            username='test_name_owner',
            email='test_mail_owner@mail.com',
            password='test_password',
        )
        self.test_user = self.User.objects.create_user(
            username='test_name',
            email='test_mail@mail.com',
            password='test_password',
        )
        self.log_form_owner = {
            'username': 'test_name_owner',
            'password': 'test_password',
        }
        self.log_form_user = {
            'username': 'test_name',
            'password': 'test_password',
        }
        self.image_path = os.path.join(
            BASE_DIR, "static/assets/img/image_test.png"
        )
        self.test_seed_data = {
            'name': 'test seed name',
            'description': 'test seed description',
            'photo': 'img_data',
            'available': True,
        }

    def create_a_seed(self):
        with open(self.image_path, 'rb') as img_data:
            self.test_seed_data['photo'] = img_data
            self.client.post(reverse('seeds:add_seed'), self.test_seed_data)
        new_seed = get_object_or_404(Seed, name=self.test_seed_data['name'])
        return new_seed

    def test_user_can_generate_a_new_message(self):
        self.client.login(**self.log_form_owner)
        seed_of_owner = self.create_a_seed()
        self.client.logout()
        self.client.login(**self.log_form_user)
        response = self.client.get(
            reverse(
                'exchange_messages:new_message',
                args=[seed_of_owner.id, self.test_seed_owner.id],
            )
        )
        self.assertTrue(
            'test_name_owner' in str(response.content)
            and 'test seed name' in str(response.content)
        )

    def test_user_can_send_a_new_message(self):
        self.client.login(**self.log_form_owner)
        seed_of_owner = self.create_a_seed()
        self.client.logout()
        self.client.login(**self.log_form_user)
        self.test_seed_data['name'] = 'test seed name2'
        self.create_a_seed()
        self.test_seed_data['name'] = 'test seed name3'
        self.test_seed_data['available'] = False
        self.create_a_seed()
        number_of_discussion_before = Discussion.objects.count()
        self.client.post(
            reverse(
                'exchange_messages:new_message',
                args=[seed_of_owner.id, self.test_seed_owner.id],
            ),
            {'message': 'exchange message'},
        )
        number_of_discussion_after = Discussion.objects.count()
        mail_subject = mail.outbox[0].subject
        self.assertTrue(
            number_of_discussion_before != number_of_discussion_after
            and self.test_seed_owner.username in mail_subject
            and self.test_user.username in mail_subject
        )

    def test_user_can_delette_a_messages(self):
        self.client.login(**self.log_form_owner)
        seed_of_owner = self.create_a_seed()
        self.client.logout()
        self.client.login(**self.log_form_user)
        self.client.post(
            reverse(
                'exchange_messages:new_message',
                args=[seed_of_owner.id, self.test_seed_owner.id],
            ),
            {'message': 'a new exchange message'},
        )
        number_of_discussion_before = Discussion.objects.count()
        discussion = get_object_or_404(Discussion, sender=self.test_user.id)
        self.client.post(
            reverse('exchange_messages:my_messages'),
            {'delete_discussion': discussion.id},
        )
        number_of_discussion_after = Discussion.objects.count()
        self.assertTrue(
            number_of_discussion_before != number_of_discussion_after
        )
    
