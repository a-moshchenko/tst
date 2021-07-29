import time
from helpers.locators import DevPageLocators


class DevPage:

    def __init__(self, browser, url):
        self.browser = browser
        self.browser.go_to(url)

    def close_pop_up(self):
        self.browser.interaction_with(DevPageLocators.CLOSE_BUTTON, clickable=True, click=True)

    def login(self):
        self.browser.interaction_with(DevPageLocators.SUBMIT_BUTTON, clickable=True, click=True)

    def open_login_form(self):
        self.browser.interaction_with(DevPageLocators.LOGIN_BUTTON, clickable=True, click=True)
        time.sleep(1)
        return self.browser.interaction_with(DevPageLocators.FORM_HEADER).text

    def input_email(self, email):
        self.browser.interaction_with(DevPageLocators.EMAIL_FIELD, text=email)
        return self.browser.interaction_with(DevPageLocators.EMAIL_FIELD).get_attribute('value')

    def input_password(self, password):
        self.browser.interaction_with(DevPageLocators.PASSWORD_FIELD, text=password)
        return self.browser.interaction_with(DevPageLocators.PASSWORD_FIELD).get_attribute('value')

    def open_join_form(self):
        self.browser.interaction_with(DevPageLocators.JOIN_BUTTON, clickable=True, click=True)
        time.sleep(1)
        return self.browser.interaction_with(DevPageLocators.FORM_HEADER).text

    def open_forgot_password_form(self):
        self.browser.interaction_with(DevPageLocators.FORGOT_PASSWORD, clickable=True, click=True)
        time.sleep(1)
        return self.browser.interaction_with(DevPageLocators.FORM_HEADER).text

    def to_registration_from_login(self):
        self.browser.interaction_with(DevPageLocators.REGISTRATION_BUTTON, clickable=True, click=True)
        time.sleep(1)
        return self.browser.interaction_with(DevPageLocators.FORM_HEADER).text

    def to_login_from_registration(self):
        self.browser.interaction_with(DevPageLocators.LOGIN_FROM_JOIN_BUTTON, clickable=True, click=True)
        time.sleep(1)
        return self.browser.interaction_with(DevPageLocators.FORM_HEADER).text

    def required_fields(self):
        return self.browser.interaction_with(DevPageLocators.DIV_ERROR)

    def visible_password(self):
        self.browser.interaction_with(DevPageLocators.SHOW_PASSWORD_BUTTON, clickable=True, click=True)
        self.browser.interaction_with(DevPageLocators.PASSWORD_FIELD)

    def incorrect_input(self, email, password):
        self.input_password(password)
        self.input_email(email)
        self.login()
        return self.browser.interaction_with(
            DevPageLocators.ERROR).text.strip() == 'Incorrect login or password. Please check again.'

    def click_term_and_conditions(self):
        pass
