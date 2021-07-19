from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config

current_date = date.today()
data = current_date.strftime("%d,%m,%Y")
browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH)
browser.set_window_size(1086, 1020)
screenshot_path = config.SCREENSHOTPATHAUTH
print("check, result")
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
registration_form_checkpoint = "/html/body/div/div[2]/div/section/div"


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"page open, Error, {e}")
        browser.close()


def open_main_paga():
    browser.get(config.SITE)
    wait_for_element(main_page_checkpoint)


def register_open():
    # открывает форму регистрации
    registration_button = browser.find_element_by_class_name("regBtn")
    registration_button.click()
    sleep(1)  # без этого слипа работает только в дебаге)
    wait_for_element(registration_form_checkpoint)
    browser.refresh()
    wait_for_element(registration_form_checkpoint)


def warning_check(element_xpath, element_name):
    if browser.find_element_by_xpath(element_xpath).get_attribute("class") == "inputError":
        print(f"requiring {element_name} alert, OK")
    else:
        print(f"requiring {element_name} alert, NotOK")


def password_confirmation_error():
    open_main_paga()
    register_open()
    # Вводим пароль и некорректное подтверждение
    password_field = browser.find_element_by_xpath("//div[4]/input")
    password_field.click()
    password_field.send_keys(config.PASSWORD)
    sleep(1)  # слип нужен для разделения ввода
    password_field.send_keys(Keys.TAB)

    password_confirm_field = browser.find_element_by_xpath("//div[6]/input")
    password_confirm_field.click()
    password_confirm_field.send_keys("secretZ2")
    password_confirm_color = password_confirm_field.get_attribute("class")
    if password_confirm_color == "inputError":
        browser.save_screenshot(f"{screenshot_path}PasswordConfirmationDevNuxbet.png")
        print("confirmation, OK")
    else:
        print("confirmation, NotOK")


def invalid_email_error():
    # Вводим емайл без собаки
    open_main_paga()
    register_open()
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("qwertry")
    registration_button = browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    warning_check("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button", "main button")
    if browser.page_source.find("Enter valid email address") > 0:
        print("e-mail errMsg, OK")
    else:
        print("e-mail errMsg, NotOK")

    # Вводим емайл без домена
    open_main_paga()
    sleep(1)
    register_open()
    sleep(1)
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("qwertry@")
    registration_button = browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    if email_field.get_attribute("class") == "inputError":
        browser.save_screenshot(f"{screenshot_path}NoDomainMailDevNuxbet.png")
        print("no domain mail, OK")
    else:
        print("no domain mail, NotOK")

    # Вводим мейл с кириллицей
    open_main_paga()
    register_open()
    sleep(1)
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("почта@домен.сру")
    browser.find_element_by_xpath("//input[2]").send_keys(config.AUTHNAME)  # вводим имя пользователя
    browser.find_element_by_xpath("//div[4]/input").send_keys(config.PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("//div[6]/input").send_keys(config.PASSWORD)  # подтверждаем пароль
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/input[4]")))  # соглашаемся с T&C
    registration_button = browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    sleep(1)  # слип нужен чтоб дать форме измениться
    if str(browser.page_source).find("Wrong"):
        browser.save_screenshot(f"{screenshot_path}CyrilykMailDevNuxbet.png")
        print("cyrylik mail, OK")
    else:
        print("cyr mail, NotOK")

    # Вводим мейл с пробелом
    open_main_paga()
    sleep(1)
    register_open()
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys('"space mail"@mail.u')
    registration_button = browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    if email_field.get_attribute("class") == "inputError":
        print("space domain, OK")
    else:
        print("space domain, NotOK")

    # Вводим ранее зарегистрированный мейл
    open_main_paga()
    sleep(1)
    register_open()
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys(config.AUTHNAME)
    browser.find_element_by_xpath("//input[2]").send_keys(config.AUTHNAME)  # вводим имя пользователя
    browser.find_element_by_xpath("//div[4]/input").send_keys(config.PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("//div[6]/input").send_keys(config.PASSWORD)  # подтверждаем пароль
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/input[4]")))  # соглашаемся с T&C
    registration_button = browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    if str(browser.page_source).find("Username/Email already exist") > 0:
        browser.save_screenshot(f"{screenshot_path}UsedMailDevNuxbet.png")
        print("used mail alert, OK")
    else:
        print("used mail alert, OK")


def reqested_fields_empty():
    # Проверка алертов на незаполненых обязательных полях
    open_main_paga()
    register_open()
    sleep(1)
    browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button"
    ).click()  # нажимаем "зарегистрироваться" в форме регистрации
    sleep(1)  # нужен чтоб форма успела обновиться
    warning_check("//form/div/div/input", "mail")
    warning_check("//input[2]", "name")  # проверяем наличие ворнинга в поле имени пользователя
    warning_check("//div[7]/input", "password")  # проверяем наличие ворнинга в поле пароля
    warning_check("//div[9]/input", "password confirmation")  # проверяем наличие ворнинга в поле подтверждения пароля
    warning_check("/html/body/div/div[2]/div/section/div/form/div/div/label", "T&C")
    browser.save_screenshot(f"{screenshot_path}EmptyFieldsDevNuxbet.png")


def login_through_auth():
    # проверка перехода на форму логина с формы регистрации
    open_main_paga()
    register_open()
    sleep(1)
    browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/div[2]/a").click()
    sleep(1)  # ждем пока форма сменится
    if str(browser.current_url) == "https://dev.nuxbet.com/login":
        print("goto login, OK")
    else:
        print("goto login, NotOK")


password_confirmation_error()
invalid_email_error()
reqested_fields_empty()
login_through_auth()
browser.close()
