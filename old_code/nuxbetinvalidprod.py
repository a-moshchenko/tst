from time import sleep
from selenium.webdriver.common.keys import Keys
import commonFunctions
import config

browser = commonFunctions.browser
screenshot_path = config.SCREENSHOT_PATH_AUTHORISATION
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
registration_form_checkpoint = "/html/body/div/div[2]/div/section/div"


def registration_form_open():
    # открывает форму регистрации
    registration_button = browser.find_element_by_class_name("regBtn")
    registration_button.click()
    sleep(1)  # без этого слипа работает только в дебаге)
    commonFunctions.wait_for_element(registration_form_checkpoint)
    browser.refresh()
    commonFunctions.wait_for_element(registration_form_checkpoint)


def warning_check(element_xpath, element_name):
    if browser.find_element_by_xpath(element_xpath).get_attribute(
            "class") == "inputError":  # проверяем наличие ворнинга в поле пароля
        print(f"required {element_name} alert, OK")
    else:
        print(f"required {element_name} alert, NotOK")


def password_confirmation_error():
    commonFunctions.open_page(config.SITE_PROD, main_page_checkpoint)
    commonFunctions.register_open(registration_form_checkpoint)
    # Вводим пароль и некорректное подтверждение
    password_field = browser.find_element_by_xpath("//input[@type='password']")
    password_field.click()
    password_field.send_keys(config.PASSWORD)
    sleep(1)  # слип нужен для разделения ввода
    password_field.send_keys(Keys.TAB)
    password_confirm_field = browser.find_element_by_xpath("(//input[@type='password'])[2]")
    password_confirm_field.click()
    password_confirm_field.send_keys("secretZ2")
    password_confirm_color = password_confirm_field.get_attribute("class")
    if password_confirm_color == "inputError":
        browser.save_screenshot(f"{screenshot_path}InvalidPasswordConfirmNuxbet.png")
        print("confirmation, OK")
    else:
        print("confirmation, NotOK")


def invalid_email_error():
    # Вводим емайл без собаки
    browser.refresh()
    # register_open()
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.click()
    email_field.send_keys("qwertry")
    registration_button = browser.find_element_by_xpath("//div[7]/button")
    registration_button.click()
    if not commonFunctions.capcha_finder():
        return None
    if email_field.get_attribute("class") == "inputError":
        print("no at mail, OK")
    else:
        print("no at mail, NotOK")
    if browser.page_source.find("Enter valid email address") > 0:
        browser.save_screenshot(f"{screenshot_path}NoEtMailNuxbet.png")
        print("e-mail errMsg, OK")
    else:
        print("e-mail errMsg, NotOK")

    # Вводим емайл без домена
    browser.refresh()
    # register_open()
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.click()
    email_field.send_keys("qwertry@")
    registration_button = browser.find_element_by_xpath("//div[7]/button")
    registration_button.click()
    if not commonFunctions.capcha_finder():
        return None
    if email_field.get_attribute("class") == "inputError":
        browser.save_screenshot(f"{screenshot_path}NoDomainNuxbet.png")
        print("no domain mail, OK")
    else:
        print("no domain mail, NotOK")

    # Вводим мейл с кириллицей
    browser.refresh()
    # register_open()
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.click()
    email_field.send_keys("почта@домен.сру")
    # browser.find_element_by_xpath("//input[2]").send_keys("autotestuser1672@mail.com")  # вводим имя пользователя
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(config.PASSWORD)  # подтверждаем пароль
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath(
        "//form/div/div/label")))  # соглашаемся с T&C
    registration_button = browser.find_element_by_xpath("//div[7]/button")
    registration_button.click()
    sleep(1)  # слип нужен чтоб дать форме измениться
    if not commonFunctions.capcha_finder():
        return None
    if browser.page_source.find("Wrong"):
        browser.save_screenshot(f"{screenshot_path}CyrylikMailNuxbet.png")
        print("cyr mail, OK")
    else:
        print("cyr mail, NotOK")

    # Вводим мейл с пробелом
    browser.refresh()
    # register_open()
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.click()
    email_field.send_keys('"space mail"@mail.u')
    registration_button = browser.find_element_by_xpath("//div[7]/button")
    registration_button.click()
    if not commonFunctions.capcha_finder():
        return None
    if email_field.get_attribute("class") == "inputError":
        browser.save_screenshot(f"{screenshot_path}SpaceMailNuxbet.png")
        print("space domain, OK")
    else:
        print("space domain, NotOK")

    # Вводим ранее зарегистрированный мейл
    browser.refresh()
    # register_open()
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.click()
    email_field.send_keys(config.AUTHORISATION_NAME)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(config.PASSWORD)  # подтверждаем пароль
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath(
        "//form/div/div/label")))  # соглашаемся с T&C
    registration_button = browser.find_element_by_xpath("//div[7]/button")
    registration_button.click()
    if not commonFunctions.capcha_finder():
        return None
    if browser.page_source.find("Username/Email already exist") > 0:
        browser.save_screenshot(f"{screenshot_path}UsedMailNuxbet.png")
        print("used mail alert, OK")
    else:
        print("used mail alert, OK")


def req_fields_empty():
    # Проверка алертов на незаполненых обязательных полях
    browser.refresh()
    # register_open()
    browser.find_element_by_xpath(
        "//div[7]/button").click()  # нажимаем "зарегистрироваться" в форме регистрации
    if not commonFunctions.capcha_finder():
        return None
    # mail_field = browser.find_element_by_xpath("//input[@type='text']")
    # print(mail_field.get_attribute("class"))  # разкомментить если нужно дебажить
    warning_check("//input[@type='text']", "mail")  # проверяем наличие ворнинга в поле имейла
    warning_check("//input[@type='password']", "password")  # проверяем наличие ворнинга в поле пароля
    warning_check(
        "(//input[@type='password'])[2]", "password confirmation")  # проверяем ворнинг в поле подтверждения пароля
    warning_check("//form/div/div/label", "T&C")  # проверяем наличие ворнинга в боксе T&C
    browser.save_screenshot(f"{screenshot_path}EmptyFieldsNuxbet.png")


def login_through_auth():
    # проверка перехода на форму логина с формы регистрации
    browser.refresh()
    # register_open()
    sleep(1)
    browser.find_element_by_xpath("//div[2]/span[2]").click()
    sleep(1)  # ждем пока форма сменится
    if browser.page_source.find("formWrap authForm") > 0:
        print("goto login, OK")
    else:
        print("goto login, NotOK")


password_confirmation_error()
invalid_email_error()
req_fields_empty()
login_through_auth()
browser.close()
