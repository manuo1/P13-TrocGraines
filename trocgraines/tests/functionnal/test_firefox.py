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
        pass

    def test_homepage(self):
        """ test simple homepage display """
        self.go_to_url_name('trocgraines:homepage')
        self.assertTrue(self.element_is_present('seed_search_form'))


    """ some methods to improve the readability of tests """

    def go_to_url_name(self, url_name):
        """ access a web page with its URL name  """
        self.driver.get(self.live_server_url + reverse(url_name))

    def element_is_present(self, id):
        try:
            self.driver.find_element_by_id(id)
            return True
        except NoSuchElementException:
            return False
