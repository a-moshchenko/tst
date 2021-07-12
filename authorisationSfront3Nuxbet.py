""""Дописать позитив флоу и восстановление пароля"""

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
registration_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"wait for element, Error, {e}, {xpath}")
        browser.close()


def open_main_page():
    browser.get(config.SFRONT3SITE)
    browser.set_window_size(1086, 1020)
    wait_for_element(main_page_checkpoint)
    sleep(1)


def open_login_form():
    browser.find_element_by_xpath("//a[contains(@href, '#')]").click()
    wait_for_element(registration_form_checkpoint)
    browser.refresh()
    wait_for_element(registration_form_checkpoint)

def login_negative_flow():
    # проверка пустых полей
    browser.find_element_by_xpath("//form/div[2]/button").click()
    sleep(1)
    if str(browser.find_element_by_xpath("//input[@type='text']").get_attribute("class")) == "inputError":
        print("no email warning, OK")
    else:
        print("no email warning, NotOK")
    if str(browser.find_element_by_xpath("//input[@type='password']").get_attribute("class")) == "inputError":
        print("no password warning, OK")
    else:
        print("no password warning, NotOK")
    if str(browser.page_source).count("This field is required") == 2:
        print("empty fields warning messages, OK")
    else:
        print("empty fields warning messages, NotOK")

    # проверка без пароля
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHNAME)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.ENTER)
    if str(browser.find_element_by_xpath("//input[@type='text']").get_attribute("class")) != "inputError":
        print("no email warning, OK")
    else:
        print("no email warning, NotOK")
    if str(browser.find_element_by_xpath("//input[@type='password']").get_attribute("class")) == "inputError":
        print("no password warning, OK")
    else:
        print("no password warning, NotOK")

    # проверка пароля без имейла
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.ENTER)
    if str(browser.find_element_by_xpath("//input[@type='text']").get_attribute("class")) == "inputError":
        print("no email warning, OK")
    else:
        print("no email warning, NotOK")
    if str(browser.find_element_by_xpath("//input[@type='password']").get_attribute("class")) != "inputError":
        print("no password warning, OK")
    else:
        print("no password warning, NotOK")

    # прверка видимого пароля
    browser.find_element_by_css_selector(".showPass").click()
    if str(browser.find_element_by_xpath("(//input[@type='text'])[2]").get_attribute("value")) == str(config.PASSWORD):
        print("visible password, OK")
    else:
        print("visible password, NotOK")

    # логин по имени пользователя (почта без домена и собаки)
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHSHORTNAME)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.ENTER)
    if str(browser.find_element_by_xpath("//input[@type='text']").get_attribute("class")) == "inputError":
        print("no email warning, OK")
    else:
        print("no email warning, NotOK")

    # проверка несуществующей почты
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("notexisting@mail.com")
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.ENTER)
    sleep(1)  # форма в это время обновляется
    if str(browser.page_source).find("Incorrect login or password. Please check again.") > 0:
        print("incorrect data warning message, OK")
    else:
        print("incorrect data warning message, NotOK")

    # логин по неправильному паролю
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='text']").clear()
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHNAME)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(str(config.PASSWORD)[1:])
    browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.ENTER)
    sleep(1)  # форма в это время обновляется
    if str(browser.page_source).find("Incorrect login or password. Please check again.") > 0:
        print("incorrect data message, OK")
    else:
        print("incorrect data message, NotOK")

    # логин гуглового пользователя по адресу почты
    browser.refresh()
    browser.find_element_by_xpath("//input[@type='text']").clear()
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.DEFAULTMAIL)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(str(config.PASSWORD)[1:])
    browser.find_element_by_xpath("//input[@type='text']").send_keys(Keys.ENTER)
    sleep(1)  # форма в это время обновляется
    if str(browser.page_source).find("This account can only be logged by Google") > 0:
        print("Google account warning message, OK")
    else:
        print("Google account warning message, NotOK")


open_main_page()
open_login_form()
sleep(1)
login_negative_flow()