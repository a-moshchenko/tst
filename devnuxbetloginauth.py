from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

SITE = "https://dev.nuxbet.com/"  # url сайта, на котором будем проводить тест
EXECUTABLE_PATH = r"C:\chromedriver\chromedriver"  # Тут указать путь к файлу драйвера браузера
browser = webdriver.Chrome(executable_path=EXECUTABLE_PATH)
RESULTS = ("check, result")
print(RESULTS)


def randnum():
    # генерит рандомную строку из четырех цыфр
    a = ""
    for i in range(4):
        a += str(random.randint(1, 9))
    return a


Uname = "autotestuser" + randnum()
PASSWD = "secretZ1"
REFCODE = "QwERty123!@#"


def final_checks():
    # Проверяет имя пользователя в форме регистрации
    print("userMail, OK")
    print("userName, OK")
    if browser.find_element_by_xpath("//div[4]/input").get_attribute("value") == PASSWD:
        print("password visibility, OK")
    else:
        print("password visibility, NotOK")
    if browser.find_element_by_xpath("//div[6]/input").get_attribute("value") == PASSWD:
        print("passwordCon visibility, OK")
    else:
        print("passwordCon visibility, NotOK")


def open(SITE):
    browser.get(SITE)
    browser.set_window_size(1086, 1020)
    sleep(2)


def auth_form_check():
    try:
        # Проверяем наличие формы авторизации
        browser.find_element_by_class_name("authForm")
        print("authForm, OK")
    except:
        # если формы нет - закрываем окно браузера и выводим ерор
        print("authForm, NoPopUp")
        browser.close()


def email_input():
    try:
        # Вводим емайл
        email_input_field = browser.find_element_by_xpath("//form/div/div/input")
        email_input_field.click()
        email_input_field.send_keys(str(Uname + "@mail.com"))
    except:
        print("E-mail input, ERROR")


def username_input():
    try:
        # Вводим юзернейм
        username_field = browser.find_element_by_xpath("//input[2]")
        username_field.click()
        username_field.send_keys(Uname)
    except:
        print("login input, ERROR")


def password_visibility_check():
    try:
        # Проверяем нескрытое отображение пароля
        password_field = browser.find_element_by_xpath("//div[4]/div")
        password_field.click()
        password_confirm_field = browser.find_element_by_xpath("//div[6]/div")
        password_confirm_field.click()
        sleep(1)
    except:
        print("Visible password ERROR")


def password_and_confirmation_input():
    try:
        # Вводим пароль и подтверждение
        password_field = browser.find_element_by_xpath("//div[4]/input")
        password_field.click()
        password_field.send_keys(PASSWD)
        sleep(1)
        password_field.send_keys(Keys.TAB)
        password_confirm_field = browser.find_element_by_xpath("//div[6]/input")
        password_confirm_field.click()
        password_confirm_field.send_keys(PASSWD)
        password_visibility_check()
    except:
        print("Password input Error")


def refCode_input_and_Check():
    try:
        ref_code_field = browser.find_element_by_xpath("//div/input[3]")
        ref_code_field.send_keys(REFCODE)
        sleep(1)
        if ref_code_field.get_attribute("value") == REFCODE:
            print("ref code, OK")
        else:
            print("refCode: ", ref_code_field.get_attribute("value"))
    except:
        print("ref code, NotOK")


def termsAndConditions_confirmation():
    try:
        # Соглашаемся с T&C
        terms_checkbox = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/input[4]")
        browser.execute_script("arguments[0].click();", terms_checkbox)
        print("T&C acepted, OK")
    except:
        print("T&C ERROR")


def registred_user_check():
    user = browser.find_element_by_xpath("//div[2]/div[3]")
    if user.text == str(Uname + "@mail.com"):
        print("main page return, OK")
    else:
        print("main page return, NotOK")


def registr_valid():
    # Выполняет регистрацию пользователя по позитив флоу с валидными даными
    registration_button = browser.find_element_by_class_name("regBtn")
    registration_button.click()
    sleep(1)

    auth_form_check()
    email_input()
    username_input()
    password_and_confirmation_input()
    refCode_input_and_Check()
    termsAndConditions_confirmation()
    final_checks()

    registration_form_button = browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_form_button.click()

    sleep(2)

    registred_user_check()
    print("Username: ", Uname)
    print("Usermail: ", Uname, "@mail.com")


open(SITE)
try:
    registr_valid()
except:
    print("registration, registration Error")
browser.close()
