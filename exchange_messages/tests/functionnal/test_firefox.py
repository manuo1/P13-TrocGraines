import os

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from exchange_messages.models import Discussion
from seeds.models import Seed
from trocgraines_config.settings.common import BASE_DIR

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless')
firefox_options.set_preference("browser.privatebrowsing.autostart", True)


class FirefoxFunctionalTestCases(LiveServerTestCase):
    """Functional tests using the Firefox web browser in headless mode."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox(options=firefox_options)
        cls.driver.implicitly_wait(30)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.driver.quit()

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(
            username="owner",
            password="testpassword",
            email="testowner@mail.com",
        )
        User.objects.create_user(
            username="user",
            password="testpassword",
            email="testuser@mail.com",
        )
        self.image_path = os.path.join(
            BASE_DIR, "static/assets/img/image_test.png"
        )
        self.test_seed_data = {
            'name': 'test seed name 2',
            'description': 'test seed description 2',
            'photo': self.image_path,
        }

    def test_user_can_create_and_delette_a_message(self):
        number_of_discussion_before = Discussion.objects.count()
        self.login_the_user(username='owner')
        seed = self.create_new_seed()
        self.go_to_url_name('authentication:logout')
        self.login_the_user(username='user')
        self.click_on_id('exchange_btn_' + str(seed.id))
        self.click_on_id('send_exchange_message_form_btn')
        number_of_discussion_while = Discussion.objects.count()
        user = get_object_or_404(get_user_model(), username='user')
        discution = get_object_or_404(Discussion, sender=user)
        self.click_on_id('discussion_' + str(discution.id) + '_delete_btn')
        self.click_on_id(
            'discussion_' + str(discution.id) + '_delete_btn_confirm'
        )
        number_of_discussion_after = Discussion.objects.count()
        self.assertTrue(
            number_of_discussion_before != number_of_discussion_while
            and number_of_discussion_while != number_of_discussion_after
            and number_of_discussion_before == number_of_discussion_after
        )

    """ some methods to improve the readability of tests """

    def create_new_seed(self):
        """add a seed in data base."""
        self.click_on_id('add_seed_btn')
        self.write_in_id('id_name', self.test_seed_data['name'])
        self.write_in_id('id_description', self.test_seed_data['description'])
        self.write_in_id('id_photo', self.test_seed_data['photo'])
        self.click_on_id('add_seed_form_btn')
        new_seed = get_object_or_404(Seed, name=self.test_seed_data['name'])
        return new_seed

    def go_to_url_name(self, url_name):
        """access a web page with its URL name."""
        self.driver.get(self.live_server_url + reverse(url_name))

    def click_on_id(self, id):
        """find element by id and click on it."""
        self.driver.find_element_by_id(id).click()

    def write_in_id(self, id, value):
        """find element by id and send keys inside."""
        element = self.driver.find_element_by_id(id)
        element.clear()
        element.send_keys(value)

    def login_the_user(self, username='testusername', password='testpassword'):
        """run the login procedure."""
        self.go_to_url_name('authentication:login')
        self.write_in_id('id_username', username)
        self.write_in_id('id_password', password)
        self.click_on_id('login_form_btn')

    def element_is_present(self, id):
        """return true if the element with this id is present."""
        try:
            self.driver.find_element_by_id(id)
            return True
        except NoSuchElementException:
            return False

    def get_html_in(self, element_id):
        """find element by id and return the html contained inside."""
        html = self.driver.find_element_by_id(element_id).get_attribute(
            'innerHTML'
        )
        return html
