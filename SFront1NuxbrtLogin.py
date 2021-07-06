from time import sleep
from pathlib import Path
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

browser = webdriver.Chrome(executable_path=Path.cwd()/"driwers"/"chromedriver.exe", options=chrome_options)
current_date = date.today()
date = current_date.strftime("%d,%m,%Y")
screenshot_path = Path.cwd()/"screenshots"/date
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
login_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"registration form open, Error, {e}")
        browser.close()


def open():
    browser.get(config.SFRONT1SITE)
    browser.set_window_size(1086, 1020)
    wait_for_element(main_page_checkpoint)
    browser.refresh()
    sleep(2)


def login_form_open():
    try:
        browser.find_element_by_class_name("loginBtn").click()
        wait_for_element(login_form_checkpoint)
    except Exception as e:
        print(f"no login button, Error, {e}")
    try:
        browser.find_element_by_xpath(login_form_checkpoint)
        print("Login form, OK")
    except Exception as e:
        print(f"Login form, OK, Error {e}")


def login_via_mail():
    login_form_open()
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHSHORTNAME)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    visible_password()
    login_button = browser.find_element_by_css_selector(".btnWrap > .mainBtn")
    login_button.click()
    wait_for_element(main_page_checkpoint)
    if str(browser.page_source).find(config.AUTHSHORTNAME):
        print(f"login, OK\ngoto main page, OK")
        browser.save_screenshot(f"{screenshot_path}LoginViaUsernameSuccessSFront1Nuxbet.png")
    else:
        print(f"login, NotOK\ngoto main page, NotOK")
        browser.save_screenshot(f"{screenshot_path}LoginViaUsernameFailSFront1Nuxbet.png")
    sleep(2)
    log_out()


def log_out():
    try:
        browser.find_element_by_css_selector(".userWrap .vs__open-indicator").click()
        sleep(1)  # нужно чтоб появилось дропдаун меню
        print("dropdown menu, OK")
        browser.save_screenshot(f"{screenshot_path}DropdownMenuSFront1Nuxbet.png")
        browser.find_element_by_xpath("//a[7]").click()
        wait_for_element(main_page_checkpoint)
        try:
            browser.find_element_by_xpath(main_page_checkpoint)
            print("Logout, OK")
        except Exception as e:
            print(f"goto main page, NotOK, Error, {e}")
    except Exception as e:
        print(f"unable to logout, Error, {e}")


def visible_password():
    try:
        browser.find_element_by_css_selector(".showPass").click()
        if browser.find_element_by_css_selector(".passWrap > input").get_attribute("value") == str(config.PASSWORD):
            browser.save_screenshot(f"{screenshot_path}PasswordVisibleSFront1Nuxbet.png")
        else:
            print("password visibility, NotOK")
    except Exception as e:
        print(f"password visibility, Error, {e}")


def login_negative_flow():
    login_form_open()
    try:
        # проверка пустых полей
        login_button = browser.find_element_by_css_selector(".btnWrap > .mainBtn")
        login_button.click()
        if str(browser.find_element_by_xpath("//input[@type='text']").get_attribute("class")) == "inputError":
            print("no username error, OK")
        else:
            print("no username error, OK")
        if str(browser.find_element_by_xpath("//input[@type='password']").get_attribute("class")) == "inputError":
            print("no password error, OK")
        else:
            print("no password error, OK")
        if str(browser.page_source).count("shortText.field_required") == 2:
            print("empty fields warning, OK")
            browser.save_screenshot(f"{screenshot_path}emptyFieldsWarningSFront1Nuxbet.png")
        else:
            print("empty fields warning, NotOK")
            browser.save_screenshot(f"{screenshot_path}emptyFieldsWarningFailSFront1Nuxbet.png")
        browser.refresh()
        wait_for_element(main_page_checkpoint)

        # проверка пустого логина
        browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
        login_button = browser.find_element_by_css_selector(".btnWrap > .mainBtn")
        login_button.click()
        if str(browser.find_element_by_xpath("//input[@type='text']").get_attribute("class")) == "inputError" and \
                str(browser.find_element_by_xpath("//input[@type='password']").get_attribute("class")) != "inputError":
            print("empty username error, OK")
            browser.save_screenshot(f"{screenshot_path}emptyUsernameWarningSFront1Nuxbet.png")
        else:
            print("empty username error, OK")
            browser.save_screenshot(f"{screenshot_path}emptyUsernameWarningFailSFront1Nuxbet.png")
        browser.refresh()
        wait_for_element(main_page_checkpoint)

        # проверка пустого поля пароля
        browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHSHORTNAME)
        login_button = browser.find_element_by_css_selector(".btnWrap > .mainBtn")
        login_button.click()
        if str(browser.find_element_by_xpath("//input[@type='text']").get_attribute("class")) != "inputError" and \
                str(browser.find_element_by_xpath("//input[@type='password']").get_attribute("class")) == "inputError":
            print("empty password error, OK")
            browser.save_screenshot(f"{screenshot_path}emptyPasswordWarningSFront1Nuxbet.png")
        else:
            print("empty password error, NotOK")
            browser.save_screenshot(f"{screenshot_path}emptyPasswordWarningFailSFront1Nuxbet.png")
        browser.refresh()
        wait_for_element(main_page_checkpoint)

        # проверка невалидного юзернейма
        browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTH_NAME_EXIST)
        browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
        login_button = browser.find_element_by_css_selector(".btnWrap > .mainBtn")
        login_button.click()
        if str(browser.find_element_by_xpath("//input[@type='text']").get_attribute("class")) == "inputError" and \
                str(browser.find_element_by_xpath("//input[@type='password']").get_attribute("class")) != "inputError":
            print("invalid username error, OK")
            browser.save_screenshot(f"{screenshot_path}emptyUsermameWarningSFront1Nuxbet.png")
        else:
            print("invalid username error, NotOK")
            browser.save_screenshot(f"{screenshot_path}emptyUsernameWarningFailSFront1Nuxbet.png")
        browser.refresh()
        wait_for_element(main_page_checkpoint)

        # проверка несуществующего пользователя
        browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.CONTROL + "a")
        browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.DELETE)
        browser.find_element_by_xpath("//input[@type='password']").send_keys(Keys.CONTROL + "a")
        browser.find_element_by_xpath("//input[@type='password']").send_keys(Keys.DELETE)
        browser.find_element_by_xpath("//input[@type='text']").send_keys("notexistingusername1")
        browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
        login_button = browser.find_element_by_css_selector(".btnWrap > .mainBtn")
        login_button.click()
        sleep(2)  # форма обновляется
        if str(browser.page_source).find("Incorrect login or password. Please check again.") > 0:
            print("incorrect authorisation data error massage, OK")
            browser.save_screenshot(f"{screenshot_path}incorrectUserDataErrorMessageSFront1Nuxbet.png")
        else:
            print("incorrect authorisation data error massage, NotOK")
            browser.save_screenshot(f"{screenshot_path}incorrectUserDataErrorMessageFailSFront1Nuxbet.png")
        browser.refresh()
        wait_for_element(main_page_checkpoint)
        forgot_password()

    except Exception as e:
        print(f"invalid data, Error, {e}")


def forgot_password():
    browser.refresh()
    sleep(3)
    browser.find_element_by_xpath("//form/div/div[2]/div[2]").click()
    sleep(1)  # нужно чтоб форма обновилась
    browser.find_element_by_css_selector(".btnWrap > .mainBtn").click()
    if str(browser.find_element_by_xpath("//input[@type='text']").get_attribute("class")) == "inputError":
        print("empty password recovery, OK")
        browser.save_screenshot(f"{screenshot_path}emptyPasswordRecoverySFront1Nuxbet.png")
    else:
        print("empty password recovery, NotOK")
        browser.save_screenshot(f"{screenshot_path}emptyPasswordRecoveryFailSFront1Nuxbet.png")
    sleep(1)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHSHORTNAME)
    browser.find_element_by_css_selector(".btnWrap > .mainBtn").click()
    sleep(1)
    if str(browser.page_source).find("shortText.your_password_recovered") > 0:
        print("password recovery, OK")
        browser.save_screenshot(f"{screenshot_path}FinishPasswordRecoverySFront1Nuxbet.png")
    else:
        print("password recovery, NotOK")
        browser.save_screenshot(f"{screenshot_path}FinishPasswordRecoveryFailSFront1Nuxbet.png")
    browser.find_element_by_class_name("closeBtn").click()
    sleep(1)  # нужно чтоб форма обновилась
    browser.find_element_by_xpath("//form/div/div[2]/div[2]").click()
    sleep(1)  # нужно чтоб форма обновилась
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
    sleep(1)
    if str(browser.current_url) == "https://sfront1.nuxbet.com/tickets/create":
        print("goto ticket creation from password recovery, OK")
    else:
        print("goto ticket creation from password recovery, NotOK")
    ticket_create()

    login_form_open()
    browser.find_element_by_xpath("//form/div/div[2]/div[2]").click()
    sleep(1)  # нужно чтоб форма обновилась
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTH_NAME_EXIST)
    sleep(1)  # нужно чтоб форма обновилась
    browser.find_element_by_css_selector(".btnWrap > .mainBtn").click()
    sleep(2)  # нужно чтоб форма обновилась
    if str(browser.current_url) == "https://sfront1.nuxbet.com/tickets/create":
        print("goto ticket creation from password recovery, OK")
    else:
        print("goto ticket creation from password recovery, NotOK")


def ticket_create():
    browser.find_element_by_xpath("//input[@type='text']").send_keys("notauser")
    browser.find_element_by_xpath("(//input[@type='text'])[2]").send_keys("notexistingmail@mail.net")
    browser.find_element_by_xpath("(//input[@type='text'])[3]").send_keys("testTicket")
    browser.find_element_by_xpath("//textarea").send_keys(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore")
    browser.save_screenshot(f"{screenshot_path}CreateTicketSFront1Nuxbet.png")
    browser.find_element_by_css_selector(".mainBtn:nth-child(1)").click()
    sleep(1)
    if str(browser.page_source).find("Thanks in advance for your patience!") > 0:
        print("ticket created, OK")
        browser.save_screenshot(f"{screenshot_path}TicketCreatedSFront1Nuxbet.png")
    else:
        print("ticket created, NotOK")
        browser.save_screenshot(f"{screenshot_path}TicketCreatedFailSFront1Nuxbet.png")
    browser.refresh()
    open()
    wait_for_element(main_page_checkpoint)
    login_form_open()
    login_via_google()


def login_via_google():
    browser.find_element_by_xpath("//img[@alt='google']").click()
    sleep(2)
    browser.find_element_by_xpath(
                "//input[@id='identifierId']").send_keys(config.DEFAULTMAIL)
    browser.find_element_by_xpath("//input[@id='identifierId']").send_keys(Keys.ENTER)
    sleep(1)  # нужно чтоб форма гугла обновилась
    browser.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input").send_keys(config.PASSWORD)
    sleep(1)
    browser.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input").send_keys(Keys.ENTER)
    wait_for_element(main_page_checkpoint)
    sleep(3)
    if str(browser.page_source).find("109693494692241829544") > 0:
        print("google login, OK")
    else:
        print("google login, NotOK")


open()
login_via_mail()
login_negative_flow()
browser.close()
