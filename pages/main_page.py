import time
import locators


class MainPage:

    def __init__(self, browser, url):
        self.browser = browser
        self.browser.go_to(url)

    def close_pop_up(self):
        self.browser.interaction_with(locators.MainPageLocators.CLOSE_BUTTON, clickable=True, click=True)

    def open_login_form(self):
        self.browser.interaction_with(locators.MainPageLocators.LOGIN_BUTTON, clickable=True, click=True)
        time.sleep(1)
        return self.browser.interaction_with(locators.MainPageLocators.FORM_HEADER).text

    def open_join_form(self):
        self.browser.interaction_with(locators.MainPageLocators.JOIN_BUTTON, clickable=True, click=True)
        time.sleep(1)
        return self.browser.interaction_with(locators.MainPageLocators.FORM_HEADER).text

    def open_forgot_password_form(self):
        self.browser.interaction_with(locators.MainPageLocators.FORGOT_PASSWORD, clickable=True, click=True)
        time.sleep(1)
        return self.browser.interaction_with(locators.MainPageLocators.FORM_HEADER).text

    def click_term_and_conditions(self):
        pass

