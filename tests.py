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
    test_page.input_login()
    test_page.input_password()
    assert config.PASSWORD == test_page.view_password()
    test_page.login()
    assert config.AUTHORISATION_NAME == test_page.get_username()

