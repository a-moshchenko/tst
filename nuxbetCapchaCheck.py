from enum import Enum
from selenium.common.exceptions import TimeoutException
import config


class Locators(str, Enum):

    GO_TO_LOGIN = "//a[@class='loginBtn']"
    INPUT_FIELD = "//input[@type='text']"
    PASSWORD_FIELD = "//input[@type='password']"
    LOGIN_BUTTON = "//button[@class='mainBtn']"
    CAPTCHA_ELEMENT = "//div[@class='rc-anchor-logo-text']"


class CaptchaCheck:

    def __init__(self, driver):
        self.driver = driver
        self.base_url = config.SITE

    def open_site(self):
        self.driver.go_to(self.base_url)

    def open_login_form(self):
        self.driver.interaction_with(Locators.GO_TO_LOGIN, clickable=True, click=True)

    def input_login(self):
        self.driver.interaction_with(Locators.INPUT_FIELD, text=config.AUTHORISATION_NAME)

    def input_password(self):
        self.driver.interaction_with(Locators.PASSWORD_FIELD, text=config.PASSWORD[1:])

    def check_captcha(self):
        for _ in range(10):
            try:
                self.driver.interaction_with(Locators.LOGIN_BUTTON, clickable=True, click=True)
            except TimeoutException:
                iframe = self.driver.interaction_with("//iframe[@id='the_iframe']")
                self.driver.switch_to_iframe(iframe)
                re_captcha_iframe = self.driver.interaction_with("//iframe[@title='reCAPTCHA']")
                return re_captcha_iframe.get_attribute('title')
