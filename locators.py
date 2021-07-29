from selenium.webdriver.common.by import By

"""LOCATORS TYPE"""

# By.CLASS_NAME
# By.NAME
# By.ID
# By.LINK_TEXT
# By.XPATH
# By.TAG_NAME
# By.PARTIAL_LINK_TEXT


class MainPageLocators(object):

    LOGIN_BUTTON = (By.CLASS_NAME, 'loginBtn')
    JOIN_BUTTON = (By.CSS_SELECTOR, '.mainBtn.regBtn')
    FORM_HEADER = (By.CSS_SELECTOR, '.formWrap .formHeader')
    CLOSE_BUTTON = (By.CLASS_NAME, 'closeBtn')
    TERM_AND_CONDITIONS = (By.XPATH, '//label[@for="agreeTerms"]/a')
    FORGOT_PASSWORD = (By.XPATH, '//div[@class="secondColor curPointer underline"]')


class LogInPageLocators(object):

    MAIN_BUTTON = (By.CLASS_NAME, 'loginBtn')
    EMAIL_FIELD = (By.XPATH, '//input[@type="text"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@type="password"]')
    DIV_ERROR = (By.XPATH, '//div[@class="error danger-color"]')
    LOGIN_BUTTON = (By.XPATH, '//button[@class="mainBtn"]')
