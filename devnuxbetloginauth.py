from time import sleep
import random
from datetime import date
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config

browser = webdriver.Chrome(executable_path=Path.cwd()/"driwers"/"chromedriver.exe")
current_date = date.today()
date = current_date.strftime("%d,%m,%Y")
screenshot_path = Path.cwd()/"screenshots"/date
print("check, result")
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div/div[1]/div/div/div"
registration_form_checkpoint = "/html/body/div/div[2]/div/section/div"
authorisation_form_checkpoint = "/html/body/div/div[2]/div/section/div"


def random_four_digits_number():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for i in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits


user_name = f"autotestuser{random_four_digits_number()}"


def final_checks():
    # Проверяет имя пользователя в форме регистрации
    print("userMail, OK")
    print("userName, OK")
    if browser.find_element_by_xpath("//div[4]/input").get_attribute("value") == config.PASSWD:
        print("password visibility, OK")
    else:
        print("password visibility, NotOK")
    if browser.find_element_by_xpath("//div[6]/input").get_attribute("value") == config.PASSWD:
        print("passwordCon visibility, OK")
    else:
        print("passwordCon visibility, NotOK")


def wait_for_element_by_xpath(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"page open, Error, {e}")
        browser.close()


def open():
    browser.get(config.SITE)
    browser.set_window_size(1086, 1020)
    wait_for_element_by_xpath(main_page_checkpoint)


def register_open():
    # открывает форму регистрации
    registration = browser.find_element_by_class_name("regBtn")
    registration.click()
    sleep(1)  # без этого слипа работает только в дебаге)
    wait_for_element_by_xpath(registration_form_checkpoint)
    browser.refresh()
    wait_for_element_by_xpath(registration_form_checkpoint)


def authorisation_form_check():
    try:
        # Проверяем наличие формы авторизации
        wait_for_element_by_xpath(authorisation_form_checkpoint)
        browser.find_element_by_class_name("authForm")
        print("authForm, OK")
    except Exception as ex:
        # если формы нет - закрываем окно браузера и выводим ерор
        print(f"authorisation form, NoPopUp, {ex}")
        browser.close()


def email_input():
    try:
        # Вводим емайл
        email_input_field = browser.find_element_by_xpath("//form/div/div/input")
        email_input_field.click()
        email_input_field.send_keys(str(f"{user_name}@mail.com"))
    except Exception as ex:
        print(f"E-mail input, ERROR, {ex}")


def username_input():
    try:
        # Вводим юзернейм
        username_field = browser.find_element_by_xpath("//input[2]")
        username_field.click()
        username_field.send_keys(user_name)
    except Exception as ex:
        print(f"login input, ERROR, {ex}")


def password_visibility_check():
    try:
        # Проверяем нескрытое отображение пароля
        password_field = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[4]/div")
        password_field.click()
        password_confirm_field = browser.find_element_by_xpath(
            "/html/body/div/div[2]/div/section/div/form/div/div/div[6]/div")
        password_confirm_field.click()
    except Exception as ex:
        print(f"Visible password ERROR, {ex}")


def password_and_confirmation_input():
    try:
        # Вводим пароль и подтверждение
        password_field = browser.find_element_by_xpath("//input[@type='password']")
        password_field.click()
        password_field.send_keys(config.PASSWD)
        password_field.send_keys(Keys.TAB)
        password_confirm_field = browser.find_element_by_xpath(
            "/html/body/div/div[2]/div/section/div/form/div/div/div[6]/input")
        password_confirm_field.click()
        password_confirm_field.send_keys(config.PASSWD)
        password_visibility_check()
    except Exception as ex:
        print(f"Password input Error, {ex}")


def referal_code_input_and_check():
    try:
        ref_code_field = browser.find_element_by_xpath("//div/input[3]")
        ref_code_field.send_keys(config.REFCODE)
        if ref_code_field.get_attribute("value") == config.REFCODE:
            print("ref code, OK")
        else:
            print(f"refCode: {ref_code_field.get_attribute('value')}")
    except Exception as ex:
        print(f"ref code, NotOK, {ex}")


def terms_and_conditions_confirmation():
    try:
        # Соглашаемся с T&C
        terms_checkbox = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/input[4]")
        browser.execute_script("arguments[0].click();", terms_checkbox)
        print("T&C acepted, OK")
    except Exception as ex:
        print(f"T&C ERROR, {ex}")


def registred_user_check():
    user = browser.find_element_by_xpath("//div[2]/div[3]")
    if user.text == str(f"{user_name}@mail.com"):
        print("main page return, OK")
    else:
        print("main page return, NotOK")


def registration_valid():
    # Выполняет регистрацию пользователя по позитив флоу с валидными даными
    register_open()
    authorisation_form_check()
    email_input()
    username_input()
    password_and_confirmation_input()
    referal_code_input_and_check()
    terms_and_conditions_confirmation()
    final_checks()
    registration_form_button = browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    browser.save_screenshot(str(f"{screenshot_path}NewUserDewnuxbet.png"))
    registration_form_button.click()
    registred_user_check()
    print(f"Username: {user_name}\nUsermail: {user_name}@mail.com")


open()
try:
    registration_valid()
except Exception as e:
    print(f"registration, registration Error, {e}")
browser.close()
