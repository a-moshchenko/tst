from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import commonFunctions
import config

browser = commonFunctions.browser
screenshot_path = config.SCREENSHOT_PATH_AUTHORISATION
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
registration_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"


def open_login_form():
    browser.find_element_by_xpath("//a[contains(@href, '#')]").click()
    commonFunctions.wait_for_element(registration_form_checkpoint)
    browser.refresh()
    commonFunctions.wait_for_element(registration_form_checkpoint)


def warning_check(element_xpath, element_name):
    if browser.find_element_by_xpath(element_xpath).get_attribute("class") == "inputError":
        print(f"no {element_name} warning, OK")
    else:
        print(f"no {element_name} warning, NotOK")


def login_negative_flow():
    # проверка пустых полей
    browser.find_element_by_xpath("//form/div[2]/button").click()
    sleep(1)
    warning_check("//input[@type='text']", "email")
    warning_check("//input[@type='password']", "password")
    if browser.page_source.count("This field is required") == 2:
        print("empty fields warning messages, OK")
    else:
        print("empty fields warning messages, NotOK")

    # проверка без пароля
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHORISATION_NAME)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.ENTER)
    if browser.find_element_by_xpath("//input[@type='text']").get_attribute("class") != "inputError":
        print("no email warning, OK")
    else:
        print("no email warning, NotOK")
    warning_check("//input[@type='password']", "password")

    # проверка пароля без имейла
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.ENTER)
    warning_check("//input[@type='text']", "email")
    if browser.find_element_by_xpath("//input[@type='password']").get_attribute("class") != "inputError":
        print("no password warning, OK")
    else:
        print("no password warning, NotOK")

    # прверка видимого пароля
    browser.find_element_by_css_selector(".showPass").click()
    if str(browser.find_element_by_xpath("(//input[@type='text'])[2]").get_attribute("value")) == config.PASSWORD:
        print("visible password, OK")
    else:
        print("visible password, NotOK")

    # логин по имени пользователя (почта без домена и собаки)
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHORISATION_NAME)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.ENTER)
    warning_check("//input[@type='text']", "email")

    # проверка несуществующей почты
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("notexisting@mail.com")
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.ENTER)
    sleep(1)  # форма в это время обновляется
    if browser.page_source.find("Incorrect login or password. Please check again.") > 0:
        print("incorrect input warning message, OK")
    else:
        print("incorrect input warning message, NotOK")

    # логин по неправильному паролю
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='text']").clear()
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHORISATION_NAME)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD[1:])
    browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.ENTER)
    sleep(1)  # форма в это время обновляется
    if browser.page_source.find("Incorrect login or password. Please check again.") > 0:
        print("incorrect login or password message, OK")
    else:
        print("incorrect login or password message, NotOK")

    # логин гуглового пользователя по адресу почты
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='text']").clear()
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.DEFAULT_MAIL)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD[1:])
    browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.ENTER)
    sleep(1)  # форма в это время обновляется
    if browser.page_source.find("This account can only be logged by Google") > 0:
        print("Google account warning message, OK")
    else:
        print("Google account warning message, NotOK")
    browser.refresh()


def login_positive_flow():
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHORISATION_NAME)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(Keys.ENTER)
    commonFunctions.wait_for_element(main_page_checkpoint)
    if browser.page_source.find(config.AUTHORISATION_NAME) > 0:
        print("email login, OK")
    else:
        print("email login, OK")
    # log out
    commonFunctions.wait_for_element(main_page_checkpoint)
    sleep(2)
    try:
        browser.find_element_by_xpath("//span[@class = 'userName ellipsis']").click()
        sleep(1)  # ждем появления дропдаyн меню
        browser.find_element_by_xpath("//a[@href='#']").click()
        commonFunctions.open_page(config.SFRONT3_SITE, main_page_checkpoint)
    except Exception as e:
        print(f"log out Error, {e}")
    print("logged out")
    browser.refresh()


def forgot_password():
    open_login_form()
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div[1]/div[2]/div[2]").click()
    commonFunctions.wait_for_element("/html/body/div/div[1]/div[2]/div/div/div/div")
    browser.find_element_by_xpath("//button[@class='mainBtn']").click()
    if browser.find_element_by_xpath("//input [@type='text']").get_attribute("class") == "inputError":
        print("Empty email field, OK")
    else:
        print("Empty email access recovery field, NotOK")
    browser.find_element_by_xpath("//input[@type = 'text']").send_keys(config.AUTHORISATION_NAME)
    browser.find_element_by_xpath("//input[@type = 'text']").send_keys(Keys.ENTER)
    sleep(1)
    if browser.page_source.find("We have sent a verification code to your email") > 0:
        print("access recovery, OK")
    else:
        print("access recovery, NotOK")

    browser.refresh()
    commonFunctions.wait_for_element(main_page_checkpoint)
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div[1]/div[2]/div[2]").click()
    commonFunctions.wait_for_element("/html/body/div/div[1]/div[2]/div/div/div/div")
    browser.find_element_by_xpath("//input[@type = 'text']").send_keys(config.AUTHORISATION_SHORT_NAME)
    browser.find_element_by_xpath("//input[@type = 'text']").send_keys(Keys.ENTER)
    sleep(1)
    if browser.page_source.find("Your password cannot be recovered, contact support.") > 0:
        print("access recovery username warning, OK")
        browser.save_screenshot(f"{screenshot_path}UsernamePasswordRecoverySFront3Nuxbet.png")
        browser.find_element_by_xpath("//button[@class='mainBtn']").click()
        sleep(2)
        if browser.current_url == f"{config.SFRONT3_SITE}tickets/create":
            print("ticket creation form, OK")
            browser.save_screenshot(f"{screenshot_path}ticketCreationFormSFront3Nuxbet.png")
        else:
            print("ticket creation form, NotOK")
            browser.save_screenshot(f"{screenshot_path}ticketCreationFormSFront3Nuxbet.png")
    else:
        print("access recovery username warning, NotOK")
        browser.save_screenshot(f"{screenshot_path}UsernamePasswordRecoverySFront3Nuxbet.png")


commonFunctions.open_page(config.SFRONT3_SITE, main_page_checkpoint)
open_login_form()
sleep(1)
login_negative_flow()
login_positive_flow()
forgot_password()
browser.close()
