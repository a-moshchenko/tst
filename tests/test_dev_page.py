import pytest
from selenium.common.exceptions import TimeoutException

from pages import DevPage
from helpers.enums import SiteUrlEnum
from helpers.helper import screenshot


@screenshot
def test_dev_page(browser, creds):

    """TEST LOGIN"""
    dev_page = DevPage(browser, SiteUrlEnum.DEV)
    # open login pop-up
    assert dev_page.open_login_form().lower() == 'log in'
    # click to forgot password
    assert dev_page.open_forgot_password_form().lower() != 'forgot password?'
    dev_page.close_pop_up()
    # empty email
    dev_page.input_password(creds.PASSWORD)
    dev_page.login()
    assert dev_page.required_fields().get_attribute('type') == 'text'
    dev_page.close_pop_up()
    # empty password
    dev_page.open_login_form()
    dev_page.input_email(creds.AUTHORISATION_NAME)
    dev_page.login()
    assert dev_page.required_fields().get_attribute('type') == 'password'
    dev_page.close_pop_up()
    # empty email and password
    dev_page.open_login_form()
    dev_page.login()
    assert dev_page.required_fields()[0].get_attribute('type') == 'text'
    assert dev_page.required_fields()[1].get_attribute('type') == 'password'
    # incorrect password correct email
    assert dev_page.incorrect_input(creds.AUTHORISATION_NAME, 'password')
    # correct password incorrect email
    assert dev_page.incorrect_input('shopopalo@super.com', creds.PASSWORD)
    assert dev_page.incorrect_input('орпваоып@super.com', creds.PASSWORD)
    assert dev_page.incorrect_input('shopopalo@super', creds.PASSWORD)
    assert dev_page.incorrect_input('shopopalo', creds.PASSWORD)
    # show password
    with pytest.raises(TimeoutException):
        dev_page.visible_password()

    """TEST REGISTRATION"""
    # click to  Registration button
    assert dev_page.to_registration_from_login().lower() == 'join now'
    dev_page.close_pop_up()
    # open registration pop-up
    assert dev_page.open_join_form().lower() == 'join now'
    # click to  Log In button
    assert dev_page.to_login_from_registration().lower() == 'log in'
    dev_page.close_pop_up()
