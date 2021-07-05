from time import sleep
from datetime import date
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

current_date = date.today()
data = current_date.strftime("%d,%m,%Y")
browser = webdriver.Chrome(executable_path=Path.cwd()/"driwers"/"chromedriver.exe")
screenshot_path = Path.cwd()/"screenshots"/data
print("check, result")
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
registration_form_checkpoint = "/html/body/div/div[2]/div/section/div"

def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except:
        print("page open, Error")
        browser.close()

def open():
    browser.get(config.SITE)
    browser.set_window_size(1086, 1020)
    wait_for_element(main_page_checkpoint)

def register_open():
    # открывает форму регистрации
    regi = browser.find_element_by_class_name("regBtn")
    regi.click()
    sleep(1) # без этого слипа работает только в дебаге)
    wait_for_element(registration_form_checkpoint)
    browser.refresh()
    wait_for_element(registration_form_checkpoint)

def password_confirmation_error():
    open()
    register_open()
    # Вводим пароль и некорректное подтверждение
    password_field = browser.find_element_by_xpath("//div[4]/input")
    password_field.click()
    password_field.send_keys(config.PASSWORD)
    sleep(1) # слип нужен для разделения ввода
    password_field.send_keys(Keys.TAB)

    password_confirn_field = browser.find_element_by_xpath("//div[6]/input")
    password_confirn_field.click()
    password_confirn_field.send_keys("secretZ2")
    password_confirn_color = password_confirn_field.get_attribute("class")
    if password_confirn_color == "inputError":
        browser.save_screenshot(str(f"{screenshot_path}PasswordConfirmationDevNuxbet.png"))
        print("confirmation, OK")
    else:
        print("confirmation, NotOK")

def invalid_email_error():
    # Вводим емайл без собаки
    open()
    register_open()
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("qwertry")
    registration_button = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    if email_field.get_attribute("class") == "inputError":
        browser.save_screenshot(str(f"{screenshot_path}NoEtMailDevNuxbet.png"))
        print("no at mail, OK")
    else:
        print("no at mail, NotOK")
    if str(browser.page_source).find("Enter valid email address") > 0:
        print("e-mail errMsg, OK")
    else:
        print("e-mail errMsg, NotOK")

    # Вводим емайл без домена
    open()
    sleep(1)
    register_open()
    sleep(1)
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("qwertry@")
    registration_button = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    if email_field.get_attribute("class") == "inputError":
        browser.save_screenshot(str(f"{screenshot_path}NoDomainMailDevNuxbet.png"))
        print("no domain mail, OK")
    else:
        print("no domain mail, NotOK")

    # Вводим мейл с кириллицей
    open()
    register_open()
    sleep(1)
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("почта@домен.сру")
    browser.find_element_by_xpath("//input[2]").send_keys("autotestuser1672@mail.com")  # вводим имя пользователя
    browser.find_element_by_xpath("//div[4]/input").send_keys(config.PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("//div[6]/input").send_keys(config.PASSWORD)  # подтверждаем пароль
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/input[4]")))  # соглашаемся с T&C
    registration_button = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    sleep(1) # слип нужен чтоб дать форме измениться
    if str(browser.page_source).find("Wrong"):
        browser.save_screenshot(str(f"{screenshot_path}CyrilykMailDevNuxbet.png"))
        print("cyrylik mail, OK")
    else:
        print("cyr mail, NotOK")

    # Вводим мейл с пробелом
    open()
    sleep(1)
    register_open()
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys('"space mail"@mail.u')
    registration_button = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    if email_field.get_attribute("class") == "inputError":
        print("space domain, OK")
    else:
        print("space domain, NotOK")

    # Вводим ранее зарегистрированный мейл
    open()
    sleep(1)
    register_open()
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("autotestuser1672@mail.com")
    browser.find_element_by_xpath("//input[2]").send_keys("autotestuser1672@mail.com")  # вводим имя пользователя
    browser.find_element_by_xpath("//div[4]/input").send_keys("secretZ1")  # вводим пароль
    browser.find_element_by_xpath("//div[6]/input").send_keys("secretZ1")  # подтверждаем пароль
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/input[4]")))  # соглашаемся с T&C
    registration_button = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    if str(browser.page_source).find("Username/Email already exist") > 0:
        browser.save_screenshot(str(f"{screenshot_path}UsedMailDevNuxbet.png"))
        print("used mail alert, OK")
    else:
        print("used mail alert, OK")

def req_fields_empty():
    # Проверка алертов на незаполненых обязательных полях
    open()
    register_open()
    sleep(1)
    browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button").click()  # нажимаем "зарегистрироваться" в форме регистрации
    sleep(1) # нужен чтоб форма успела обновиться
    mail_field = browser.find_element_by_xpath("//form/div/div/input")
    # print(mail_field.get_attribute("class"))  # разкомментить если нужно дебажить
    if mail_field.get_attribute("class") == "inputError":  # проверяем наличие ворнинга в поле имейла
        print("requiring mail alert, OK")
    else:
        print("requiring mail alert, NotOK")
    if str(browser.find_element_by_xpath("//input[2]").get_attribute(
            "class")) == "inputError":  # проверяем наличие ворнинга в поле имени пользователя
        print("requiring name alert, OK")
    else:
        print("requiring name alert, NotOK")
    if str(browser.find_element_by_xpath("//div[7]/input").get_attribute(
            "class")) == "inputError":  # проверяем наличие ворнинга в поле пароля
        print("requiring password alert, OK")
    else:
        print("requiring password alert, NotOK")
    if str(browser.find_element_by_xpath("//div[9]/input").get_attribute(
            "class")) == "inputError":  # проверяем наличие ворнинга в поле подтверждения пароля
        print("requiring password confirmation alert, OK")
    else:
        print("requiring password confirmation alert, NotOK")
    if str(browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/label").get_attribute(
            "class")) == "inputError":  # проверяем наличие ворнинга в боксе T&C
        browser.save_screenshot(str(f"{screenshot_path}EmptyFieldsDevNuxbet.png"))
        print("required T&C alert, OK")
    else:
        print("required T&C alert, NotOK")

def login_through_auth():
    # проверка перехода на форму логина с формы регистрации
    open()
    register_open()
    sleep(1)
    browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/div[2]/a").click()
    sleep(1) # ждем пока форма сменится
    if str(browser.current_url) == "https://dev.nuxbet.com/login":
        print("goto login, OK")
    else:
        print("goto login, NotOK")

password_confirmation_error()
invalid_email_error()
req_fields_empty()
login_through_auth()
browser.close()