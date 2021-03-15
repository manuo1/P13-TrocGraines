from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

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

    def test_user_can_login_and_logout(self):
        """test if user can login and logout."""
        self.login_the_user()
        self.click_on_id('logout_btn')
        self.assertTrue(self.element_is_present('login_btn'))


    """ some methods to improve the readability of tests """

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
        self.go_to_url_name('trocgraines:homepage')
        self.click_on_id('login_btn')
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
