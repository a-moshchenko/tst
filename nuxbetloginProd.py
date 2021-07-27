from enum import Enum
import time
import config


class Locators(str, Enum):

    GO_TO_LOGIN = "//a[@class='loginBtn']"
    LOGIN_FORM = "//div[@class='formHeader flexCenter']/h2"
    INPUT_FIELD = "//input[@type='text']"
    PASSWORD_FIELD = "//input[@type='password']"
    LOGIN_BUTTON = "//button[@class='mainBtn']"
    VIEW_PASSWORD_BUTTON = "//div[@class='showPass curPointer']"
    USERNAME = "//span[@class='userName ellipsis']"
    ERROR_MESSAGE = "//div[@class='error danger-color']"
    INCORRECT_INPUT = "//div[@class='error']"
    DROP_DOWN = "//div[@class='userWrap curPointer logined allBtn']"
    LOGOUT = "//a[@href='#']"


class LoginTest:

    def __init__(self, driver):
        self.driver = driver
        self.base_url = config.SITE_PROD

    def open_site(self):
        self.driver.go_to(self.base_url)

    def open_login_form(self):
        self.driver.interaction_with(Locators.GO_TO_LOGIN, clickable=True, click=True)
        time.sleep(.3)
        return self.driver.interaction_with(Locators.LOGIN_FORM).text

    def valid_login(self):
        self.driver.interaction_with(Locators.INPUT_FIELD, text='some_text')
        self.log_in()
        return self.driver.interaction_with(Locators.ERROR_MESSAGE)

    def incorrect_login(self):
        self.driver.interaction_with(Locators.INPUT_FIELD, text=config.AUTHORISATION_NAME[1:])
        self.input_password()
        self.log_in()
        return self.driver.interaction_with(Locators.INCORRECT_INPUT).text

    def incorrect_password(self):
        self.input_login()
        self.driver.interaction_with(Locators.PASSWORD_FIELD, text=config.AUTHORISATION_NAME)
        self.log_in()
        return self.driver.interaction_with(Locators.INCORRECT_INPUT).text

    def input_login(self):
        self.driver.interaction_with(Locators.INPUT_FIELD, text=config.AUTHORISATION_NAME)

    def input_password(self):
        self.driver.interaction_with(Locators.PASSWORD_FIELD.format('password'), text=config.PASSWORD)

    def view_password(self):
        self.driver.interaction_with(Locators.VIEW_PASSWORD_BUTTON, clickable=True, click=True)
        return self.driver.interaction_with(Locators.INPUT_FIELD)[1].get_attribute("value")

    def log_in(self):
        self.driver.interaction_with(Locators.LOGIN_BUTTON, clickable=True, click=True)

    def get_username(self):
        return self.driver.interaction_with(Locators.USERNAME).text

    def log_out(self):
        self.driver.interaction_with(Locators.DROP_DOWN, clickable=True, click=True)
        self.driver.interaction_with(Locators.LOGOUT, clickable=True, click=True)
        return self.driver.interaction_with(Locators.GO_TO_LOGIN).text

