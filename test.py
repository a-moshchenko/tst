import pages


def test_main_page(browser, urls):
    for url in urls.values():
        main_page = pages.MainPage(browser, url)
        assert main_page.open_login_form().lower() == 'log in'
        assert main_page.open_forgot_password_form().lower() == 'forgot password?'
        main_page.close_pop_up()
        main_page.close_pop_up()
        assert main_page.open_join_form().lower() == 'join now'
        main_page.click_term_and_conditions()
        # assert main_page.click_term_and_conditions() == f'{config.SITE}page/terms_of_use'
        main_page.close_pop_up()


def test_login_page(browser, urls, creds):
    for url in urls.values():
        login_page = pages.LoginPage(browser, url)
        login_page.open_login_form()
        assert 2 == len(login_page.required_fields())
        assert creds.AUTHORISATION_NAME == login_page.input_email(creds.AUTHORISATION_NAME)
        assert creds.PASSWORD == login_page.input_password(creds.PASSWORD)
        login_page.login()
        # login_page.input_email_with_cyrillic()


def test_join_page(browser, urls, creds):
    pass