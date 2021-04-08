from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class TestAuthenticationViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.test_user_1 = self.User.objects.create_user(
            username='test_name',
            email='test_mail@mail.com',
            password='test_password',
        )
        self.reg_form = {
            'username': 'test_name_2',
            'email': 'test_mail_2@mail.com',
            'password1': 'test_password_2',
            'password2': 'test_password_2',
        }
        self.log_form = {'username': 'test_name', 'password': 'test_password'}

    def test_login_succes(self):
        response = self.client.post(
            reverse('authentication:login'), self.log_form
        )
        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, True)
        self.assertRedirects(response, reverse('trocgraines:homepage'))

    def test_login_fail(self):
        self.log_form['password'] = 'wrong_password'
        self.client.post(
            reverse('authentication:login'), self.log_form
        )
        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, False)

    def test_registration_succes(self):
        self.client.post(
            reverse('authentication:signup'), self.reg_form
        )
        self.assertTrue(
            self.User.objects.filter(
                username=self.reg_form['username']
            ).exists()
            and self.User.objects.filter(email=self.reg_form['email']).exists()
        )

    def test_registration_failure(self):
        self.reg_form['password2'] = 'wrong_password_2'
        self.client.post(
            reverse('authentication:signup'), self.reg_form
        )
        self.assertFalse(
            self.User.objects.filter(
                username=self.reg_form['username']
            ).exists()
        )

    def test_logout_view_when_user_is_authenticated(self):
        self.client.login(**self.log_form)
        self.client.get(reverse('authentication:logout'))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous)

    def test_if_user_can_change_display_personnal_info(self):
        self.client.login(**self.log_form)
        response = self.client.get(
            reverse('authentication:personal_informations')
        )
        self.assertTemplateUsed(response, 'personal_informations.html')

    def test_if_user_can_display_personnal_info_update(self):
        self.client.login(**self.log_form)
        response = self.client.get(
            reverse('authentication:personal_informations_update')
        )
        self.assertTemplateUsed(response, 'personal_informations_update.html')

    def test_if_user_can_change_their_personnal_info(self):
        self.client.login(**self.log_form)
        new_data_form = {
            'username_update': 'test_name_3',
            'email_update': 'test_mail_3@mail.com',
        }
        self.client.post(
            reverse('authentication:personal_informations_update'),
            new_data_form,
        )
        modified_user = auth.get_user(self.client)
        self.assertTrue(
            modified_user.username == new_data_form['username_update']
            and modified_user.email == new_data_form['email_update']
        )

    def test_if_user_can_change_his_password(self):
        self.client.login(**self.log_form)
        new_password_form = {
            'old_password': 'test_password',
            'new_password1': 'new_test_password',
            'new_password2': 'new_test_password',
        }
        self.client.post(
            reverse('authentication:password_update'), new_password_form
        )
        self.client.get(reverse('authentication:logout'))
        self.log_form['password'] = 'new_test_password'
        self.client.post(
            reverse('authentication:login'), self.log_form
        )
        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, True)
