from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config

browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH)
browser.set_window_size(1086, 1020)
current_date = date.today()
data = current_date.strftime("%d,%m,%Y")
screenshot_path = config.SCREENSHOTPATHAUTH
print("check, result")
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
redistration_form_checkpoint = "/html/body/div/div[2]/div/section/div"


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"page open, Error, {e}")
        browser.close()


def open_main_page():
    browser.get("https://nuxbet.com/")
    browser.refresh()
    wait_for_element(main_page_checkpoint)


def registration_form_open():
    # открывает форму регистрации
    registration_button = browser.find_element_by_class_name("regBtn")
    registration_button.click()
    sleep(1)  # без этого слипа работает только в дебаге)
    wait_for_element(redistration_form_checkpoint)
    browser.refresh()
    wait_for_element(redistration_form_checkpoint)


def warning_check(element_xpath, element_name):
    if browser.find_element_by_xpath(element_xpath).get_attribute(
            "class") == "inputError":  # проверяем наличие ворнинга в поле пароля
        print(f"required {element_name} alert, OK")
    else:
        print(f"required {element_name} alert, NotOK")


def password_confirmation_error():
    open_main_page()
    registration_form_open()
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
    open_main_page()
    # register_open()
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.click()
    email_field.send_keys("qwertry")
    registration_button = browser.find_element_by_xpath("//div[7]/button")
    registration_button.click()
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
    open_main_page()
    # register_open()
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.click()
    email_field.send_keys("qwertry@")
    registration_button = browser.find_element_by_xpath("//div[7]/button")
    registration_button.click()
    if email_field.get_attribute("class") == "inputError":
        browser.save_screenshot(f"{screenshot_path}NoDomainNuxbet.png")
        print("no domain mail, OK")
    else:
        print("no domain mail, NotOK")

    # Вводим мейл с кириллицей
    open_main_page()
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
    if browser.page_source.find("Wrong"):
        browser.save_screenshot(f"{screenshot_path}CyrylikMailNuxbet.png")
        print("cyr mail, OK")
    else:
        print("cyr mail, NotOK")

    # Вводим мейл с пробелом
    open_main_page()
    # register_open()
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.click()
    email_field.send_keys('"space mail"@mail.u')
    registration_button = browser.find_element_by_xpath("//div[7]/button")
    registration_button.click()
    if email_field.get_attribute("class") == "inputError":
        browser.save_screenshot(f"{screenshot_path}SpaceMailNuxbet.png")
        print("space domain, OK")
    else:
        print("space domain, NotOK")

    # Вводим ранее зарегистрированный мейл
    open_main_page()
    # register_open()
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.click()
    email_field.send_keys(config.AUTHNAME)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(config.PASSWORD)  # подтверждаем пароль
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath(
        "//form/div/div/label")))  # соглашаемся с T&C
    registration_button = browser.find_element_by_xpath("//div[7]/button")
    registration_button.click()
    if browser.page_source.find("Username/Email already exist") > 0:
        browser.save_screenshot(f"{screenshot_path}UsedMailNuxbet.png")
        print("used mail alert, OK")
    else:
        print("used mail alert, OK")


def req_fields_empty():
    # Проверка алертов на незаполненых обязательных полях
    open_main_page()
    # register_open()
    browser.find_element_by_xpath(
        "//div[7]/button").click()  # нажимаем "зарегистрироваться" в форме регистрации
    sleep(1)  # нужен чтоб форма успела обновиться
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
    open_main_page()
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
