import os
from trocgraines_config.settings.common import BASE_DIR
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from seeds.models import Seed

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
            username="testusername",
            password="testpassword",
            email="testusername@mail.com",
        )
        self.image_path = os.path.join(
            BASE_DIR,
            "static/assets/img/image_test.png"
        )
        self.test_seed_data = {
            'name': 'test seed name 2',
            'description': 'test seed description 2',
            'photo': self.image_path,
        }

    def test_user_can_add_a_seed(self):
        """ test if user can add a seed """
        self.login_the_user()
        new_seed = self.create_new_seed()
        html = self.get_html_in("my_seeds_container")
        self.assertTrue(
            self.test_seed_data['name'] in html
            and self.test_seed_data['description'] in html
            and str(new_seed.photo) in html
        )

    def test_user_can_delette_a_seed(self):
        """ test if user can delete a seed """
        self.login_the_user()
        new_seed = self.create_new_seed()
        self.click_on_id("seed_" + str(new_seed.id) + "_delete_btn")
        self.click_on_id("seed_" + str(new_seed.id) + "_delete_btn_confirm")
        html = self.get_html_in("my_seeds_container")
        self.assertTrue(
            self.test_seed_data['name'] not in html
            and self.test_seed_data['description'] not in html
            and str(new_seed.photo) not in html
        )

    def test_user_can_change_availability_of_a_seed(self):
        """ test if user can change availability of a seed """
        self.login_the_user()
        new_seed = self.create_new_seed()
        self.click_on_id("change_seed_" + str(new_seed.id) + "_availability_btn")
        html = self.get_html_in("my_seeds_container")
        self.assertTrue(
            "Cette graine n'est pas échangeable" in html
        )
        self.click_on_id("change_seed_" + str(new_seed.id) + "_availability_btn")
        html = self.get_html_in("my_seeds_container")
        self.assertTrue(
            "Cette graine est échangeable" in html
        )

    """ some methods to improve the readability of tests """

    def create_new_seed(self):
        """ add a seed in data base """
        self.click_on_id('add_seed_btn')
        self.write_in_id('id_name', self.test_seed_data['name'])
        self.write_in_id('id_description', self.test_seed_data['description'])
        self.write_in_id('id_photo', self.test_seed_data['photo'])
        self.click_on_id('add_seed_form_btn')
        new_seed = get_object_or_404(
                        Seed,
                        name=self.test_seed_data['name']
                    )
        return new_seed


    def go_to_url_name(self, url_name):
        """ access a web page with its URL name  """
        self.driver.get(self.live_server_url + reverse(url_name))

    def click_on_id(self, id):
        """ find element by id and click on it """
        self.driver.find_element_by_id(id).click()

    def write_in_id(self, id, value):
        """ find element by id and send keys inside """
        element = self.driver.find_element_by_id(id)
        element.clear()
        element.send_keys(value)

    def login_the_user(self, username='testusername', password='testpassword'):
        """ run the login procedure  """
        self.go_to_url_name('authentication:login')
        self.write_in_id('id_username', username)
        self.write_in_id('id_password', password)
        self.click_on_id('login_form_btn')

    def element_is_present(self, id):
        """ return true if the element with this id is present """
        try:
            self.driver.find_element_by_id(id)
            return True
        except NoSuchElementException:
            return False

    def get_html_in(self, element_id):
        """ find element by id and return the html contained inside """
        html = self.driver.find_element_by_id(element_id).get_attribute(
            'innerHTML'
        )
        return html
