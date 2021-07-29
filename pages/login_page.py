import time
import locators


class LoginPage:

    def __init__(self, browser, url):
        self.browser = browser
        self.browser.go_to(url)

    def login(self):
        self.browser.interaction_with(locators.LogInPageLocators.LOGIN_BUTTON, clickable=True, click=True)

    def open_login_form(self):
        self.browser.interaction_with(locators.LogInPageLocators.MAIN_BUTTON, clickable=True, click=True)
        time.sleep(1)
        return self.browser.interaction_with(locators.MainPageLocators.FORM_HEADER).text

    def input_email(self, email):
        self.browser.interaction_with(locators.LogInPageLocators.EMAIL_FIELD, text=email)
        return self.browser.interaction_with(locators.LogInPageLocators.EMAIL_FIELD).get_attribute('value')

    def input_password(self, password):
        self.browser.interaction_with(locators.LogInPageLocators.PASSWORD_FIELD, text=password)
        return self.browser.interaction_with(locators.LogInPageLocators.PASSWORD_FIELD).get_attribute('value')

    def required_fields(self):
        self.login()
        return [i.text for i in self.browser.interaction_with(locators.LogInPageLocators.DIV_ERROR) if 'required' in i.text]

    def input_email_with_cyrillic(self):
        self.browser.interaction_with(locators.LogInPageLocators.EMAIL_FIELD, text='эмейл@эмейл.ком')



