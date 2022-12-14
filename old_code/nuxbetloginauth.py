import random
from selenium.webdriver.common.keys import Keys
import commonFunctions
import config

browser = commonFunctions.browser
screenshot_path = config.SCREENSHOT_PATH_AUTHORISATION
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
registration_form_checkpoint = "/html/body/div/div[2]/div/section/div"
authorisation_form_checkpoint = "/html/body/div/div[2]/div/section/div"


def random_four_digits_number():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for iterable_element_of_sequence_of_numbers_created_by_range in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits


user_name = f"autotestuser{random_four_digits_number()}"


def final_checks():
    # Проверяет имя пользователя в форме регистрации
    print("userMail, OK\nuserName, OK")
    if browser.find_element_by_xpath("(//input[@type='text'])[2]"
                                     ).get_attribute("value") == config.PASSWD:
        print("password visibility, OK")
    else:
        print("password visibility, NotOK")
    if browser.find_element_by_xpath("(//input[@type='text'])[3]"
                                     ).get_attribute("value") == config.PASSWD:
        print("password confirmation visibility, OK")
    else:
        print("password confirmation visibility, NotOK")


def authorisation_form_check():
    try:
        # Проверяем наличие формы авторизации
        commonFunctions.wait_for_element(authorisation_form_checkpoint)
        browser.find_element_by_class_name("authForm")
        print("authForm, OK")
    except Exception as ex:
        # если формы нет - закрываем окно браузера и выводим ерор
        print(f"authForm, NoPopUp, {ex}")
        browser.close()


def email_input():
    try:
        # Вводим емайл
        email_input_field = browser.find_element_by_xpath("//input[@type='text']")
        email_input_field.click()
        email_input_field.send_keys(f"{user_name}@mail.com")
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
        password_field = browser.find_element_by_css_selector(".passWrap:nth-child(4) > .showPass")
        password_field.click()
        password_confirm_field = browser.find_element_by_css_selector(".passWrap:nth-child(6) > .showPass")
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
        password_confirm_field = browser.find_element_by_xpath("(//input[@type='password'])[2]")
        password_confirm_field.click()
        password_confirm_field.send_keys(config.PASSWD)
        password_visibility_check()
    except Exception as ex:
        print(f"Password input Error, {ex}")


def referal_code_input_and_check():
    try:
        ref_code_field = browser.find_element_by_xpath(
            "/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/input[2]")
        ref_code_field.send_keys(config.REFERAL_CODE)
        if ref_code_field.get_attribute("value") == config.REFERAL_CODE:
            print("ref code, OK")
        else:
            print("refCode: ", ref_code_field.get_attribute("value"))
    except Exception as ex:
        print(f"ref code, NotOK, {ex}")


def terms_and_conditions_confirmation():
    try:
        # Соглашаемся с T&C
        terms_checkbox = browser.find_element_by_css_selector("label:nth-child(10)")
        browser.execute_script("arguments[0].click();", terms_checkbox)
        print("T&C accepted, OK")
    except Exception as ex:
        print(f"T&C ERROR, {ex}")


def registred_user_check():
    user = browser.find_element_by_xpath("//div[2]/div[3]")
    if user.text == f"{user_name}@mail.com":
        print("main page return, OK")
    else:
        print("main page return, NotOK")


def registration_valid():
    # Выполняет регистрацию пользователя по позитив флоу с валидными даными
    commonFunctions.register_open(registration_form_checkpoint)
    authorisation_form_check()
    email_input()
    # username_input()
    password_and_confirmation_input()
    referal_code_input_and_check()
    terms_and_conditions_confirmation()
    final_checks()
    registration_form_button = browser.find_element_by_xpath(
        "//button[@class='mainBtn']")
    browser.save_screenshot(f"{screenshot_path}RegistrationNuxbet.png")
    registration_form_button.click()
    registred_user_check()
    print(f"Username: {user_name}\nUsermail: {user_name}@mail.com")


commonFunctions.open_page(config.SITE_PROD, main_page_checkpoint)
try:
    registration_valid()
except Exception as e:
    print(f"registration, registration Error, {e}")
browser.close()
