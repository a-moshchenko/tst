from nuxbetCapchaCheck import CaptchaCheck
from creator import LoginTest
import pytest
import config


def test_captcha_check(browser):
    test_page = CaptchaCheck(browser)
    test_page.open_site()
    test_page.open_login_form()
    test_page.input_login()
    test_page.input_password()
    assert "reCAPTCHA" == test_page.check_captcha()


def test_login_prod(browser):
    test_page = LoginTest(browser)
    test_page.open_site()
    assert 'Log In' == test_page.open_login_form()
    error_messages = test_page.valid_login()
    assert 'Enter valid email address' == error_messages[0].text
    assert 'This field is required' == error_messages[1].text
    assert 'Incorrect login or password. Please check again.' == test_page.incorrect_login().strip()
    assert 'Incorrect login or password. Please check again.' == test_page.incorrect_password().strip()
    test_page.input_login()
    test_page.input_password()
    assert config.PASSWORD == test_page.view_password()
    test_page.log_in()
    assert config.AUTHORISATION_NAME == test_page.get_username()
    assert 'Log In' == test_page.log_out()


