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
        self.click_on_id('my_account_btn')
        self.click_on_id('logout_btn')
        self.click_on_id('my_account_btn')
        self.assertTrue(self.element_is_present('login_btn'))

    def test_user_can_create_an_account(self):
        """test if user can create an account and login with."""
        self.go_to_url_name('authentication:signup')
        self.write_in_id('id_username', 'testusername2')
        self.write_in_id('id_email', 'testusername2@mail.com')
        self.write_in_id('id_password1', 'Testpassword1234')
        self.write_in_id('id_password2', 'Testpassword1234')
        self.click_on_id('signup_form_btn')
        self.click_on_id('my_account_btn')
        self.click_on_id('logout_btn')
        self.login_the_user('testusername2', 'Testpassword1234')
        self.click_on_id('my_account_btn')
        self.assertTrue(self.element_is_present('my_personal_infos_btn'))

    def test_user_can_modify_their_personal_information(self):
        """test if the user can modify their personal information."""
        self.login_the_user('testusername', 'testpassword')
        self.click_on_id('my_account_btn')
        self.click_on_id('my_personal_infos_btn')
        self.click_on_id('personal_info_update_btn')
        self.write_in_id('id_username_update', 'testusername3')
        self.write_in_id('id_email_update', 'testusername3@mail.com')
        self.click_on_id('personal_info_update_done_btn')
        username_form = self.get_html_in('div_id_username_update')
        mail_form = self.get_html_in('div_id_email_update')
        self.assertTrue(
            "testusername3" in username_form
            and "testusername3@mail.com" in mail_form
        )

    def test_user_can_change_his_password(self):
        """test if the user can change his password."""
        self.login_the_user('testusername', 'testpassword')
        self.click_on_id('my_account_btn')
        self.click_on_id('my_personal_infos_btn')
        self.click_on_id('password_update_btn')
        self.write_in_id('id_old_password', 'testpassword')
        self.write_in_id('id_new_password1', 'Testpassword1234')
        self.write_in_id('id_new_password2', 'Testpassword1234')
        self.click_on_id('password_update_done_btn')
        self.go_to_url_name('authentication:logout')
        self.login_the_user('testusername', 'Testpassword1234')
        welcom_message = self.get_html_in('info_messages')
        self.assertTrue(
            "Content de vous revoir testusername" in welcom_message
        )

    """ some methods to improve the readability of tests """

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
