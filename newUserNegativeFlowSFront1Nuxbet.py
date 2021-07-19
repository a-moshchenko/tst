from time import sleep
import random
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH, options=chrome_options)
browser.set_window_size(1086, 1020)
current_date = date.today()
date = current_date.strftime("%d,%m,%Y")
screenshot_path = config.SCREENSHOTPATHAUTH
authorisation_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"


def random_four_digits_number():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for i in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits


user_name = f"autotestuser{random_four_digits_number()}"


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"registration form open, Error, {e}")
        browser.close()


def authorisation_form_open():
    sleep(1)
    browser.find_element_by_css_selector(".regBtn").click()
    wait_for_element(authorisation_form_checkpoint)
    browser.refresh()
    wait_for_element(authorisation_form_checkpoint)


def open_main_page():
    browser.get(config.SFRONT1SITE)
    wait_for_element(main_page_checkpoint)
    browser.refresh()


def warning_check(object_address, checked_object):
    if browser.find_element_by_xpath(object_address).get_attribute("class") == "inputError":
        print(f"no {checked_object} warning, OK")
    else:
        print(f"no {checked_object} warning, NotOK")


def negative_flow_authorization():
    # проверяем пустые поля
    authorisation_form_open()
    browser.find_element_by_xpath("//div[6]/button").click()
    warning_check("//input[@type='text']", "username")
    warning_check("//input[@type='password']", "password")
    warning_check("(//input[@type='password'])[2]", "password confirmation")
    warning_check("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/label", "T&C confirmation")
    browser.save_screenshot(f"{screenshot_path}EmptyFieldsSFront1Nuxbet.png")

    # проверяем без паролей
    open_main_page()
    # auth_open()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("autotestuser0000")
    browser.find_element_by_xpath("//div[6]/button").click()
    if browser.find_element_by_xpath("//input[@type='text']").get_attribute("class") != "inputError":
        print("no username warning, OK")
    else:
        print("no username warning, NotOK")

    warning_check("//input[@type='password']", "password")
    warning_check("(//input[@type='password'])[2]", "password confirmation")
    warning_check("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/label", "T&C confirmation")
    if browser.page_source.find("shortText.field_required") > 0 or browser.page_source.find(
            "This field is required") > 0:
        print("required field message, OK")
    else:
        print("required field message, NotOK")
    browser.save_screenshot(f"{screenshot_path}EmptyPasswordsSFront1Nuxbet.png")

    # проверяем с неправильным подтверждением пароля
    open_main_page()
    # auth_open()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("autotestuser0000")
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("secretZ2")
    browser.find_element_by_css_selector(".passWrap:nth-child(4) > .showPass").click()
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[5]/div").click()
    warning_check("(//input[@type='text'])[3]", "password confirmation")
    browser.save_screenshot(f"{screenshot_path}WrongPasswordConfirmationSFront1Nuxbet.png")

    # проверяем с нечекнутым T&C боксом
    open_main_page()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("autotestuser0000")
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("//div[6]/button").click()
    warning_check("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/label", "T&C confirmation")

    # проверяем киррилицу в поле юзернейм
    open_main_page()
    # auth_open()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("юзернейм")
    warning_check("//input[@type='text']", "cyrylik username")
    browser.save_screenshot(f"{screenshot_path}CyrylikUsernameSFront1Nuxbet.png")

    # проверяем ранее зарегистрированный юзернейм
    open_main_page()
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHSHORTNAME)
    browser.find_element_by_xpath("//input[@type='password']").send_keys("secretZ2")
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("secretZ2")
    try:
        terms_checkbox = browser.find_element_by_xpath("//form/div/div/label")
        browser.execute_script("arguments[0].click();", terms_checkbox)
    except Exception as e:
        print(f"T&C Error, {e}")
    browser.find_element_by_xpath("//div[6]/button").click()
    sleep(1)  # нужно чтоб форма обновилась
    if browser.page_source.find("Username/Email already exist") > 0:
        print("ExistingUser warning, OK")
    else:
        print("ExistingUser warning, NotOK")
    browser.save_screenshot(f"{screenshot_path}ExistingUsernameSFront1Nuxbet.png")


open_main_page()
negative_flow_authorization()
browser.close()
