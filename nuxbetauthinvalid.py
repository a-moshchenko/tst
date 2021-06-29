from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH)
print("check, result")

def open():
    browser.get(config.SITE)
    browser.set_window_size(1086, 1020)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/section[4]/header"))
        )
    except:
        print("page open, Error")
        browser.close()

def register_open():
    # открывает форму регистрации
    regi = browser.find_element_by_class_name("regBtn")
    regi.click()
    sleep(1) # без этого слипа работает только в дебаге)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/section/div"))
        )
    except:
        print("registr form open, Error")
        browser.close()
    browser.refresh()
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/section/div"))
        )
    except:
        print("registr form open, Error")
        browser.close()

def password_confirmation_error():
    open()
    register_open()
    # Вводим пароль и некорректное подтверждение
    password_field = browser.find_element_by_xpath("//div[4]/input")
    password_field.click()
    password_field.send_keys("secretZ1")
    sleep(1) # слип нужен для разделения ввода
    password_field.send_keys(Keys.TAB)

    password_confirn_field = browser.find_element_by_xpath("//div[6]/input")
    password_confirn_field.click()
    password_confirn_field.send_keys("secretZ2")
    password_confirn_color = password_confirn_field.get_attribute("class")
    if password_confirn_color == "inputError":
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
        print("no at mail, OK")
    else:
        print("no at mail, NotOK")
    if str(browser.page_source).find("Enter valid email address") > 0:
        print("e-mail errMsg, OK")
    else:
        print("e-mail errMsg, NotOK")

    # Вводим емайл без домена
    open()
    register_open()
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("qwertry@")
    registration_button = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    if email_field.get_attribute("class") == "inputError":
        print("no domain mail, OK")
    else:
        print("no domain mail, NotOK")

    # Вводим мейл с кириллицей
    open()
    register_open()
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("почта@домен.сру")
    browser.find_element_by_xpath("//input[2]").send_keys("autotestuser1672@mail.com")  # вводим имя пользователя
    browser.find_element_by_xpath("//div[4]/input").send_keys("secretZ1")  # вводим пароль
    browser.find_element_by_xpath("//div[6]/input").send_keys("secretZ1")  # подтверждаем пароль
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/input[4]")))  # соглашаемся с T&C
    registration_button = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    sleep(1) # слип нужен чтоб дать форме измениться
    if str(browser.page_source).find("Wrong"):
        print("cyr mail, OK")
    else:
        print("cyr mail, NotOK")

    # Вводим мейл с пробелом
    open()
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
        print("used mail alert, OK")
    else:
        print("used mail alert, OK")


def req_fields_empty():
    # Проверка алертов на незаполненых обязательных полях
    open()
    register_open()
    browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button").click()  # нажимаем "зарегистрироваться" в форме регистрации
    sleep(1) # нужен чтоб форма успела обновиться
    mail_field = browser.find_element_by_xpath("//form/div/div/input")
    # print(mail_field.get_attribute("class"))  # разкомментить если нужно дебажить
    if mail_field.get_attribute("class") == "inputError":  # проверяем наличие ворнинга в поле имейла
        print("req mail alert, OK")
    else:
        print("req mail alert, NotOK")
    if str(browser.find_element_by_xpath("//input[2]").get_attribute(
            "class")) == "inputError":  # проверяем наличие ворнинга в поле имени пользователя
        print("req name alert, OK")
    else:
        print("req name alert, NotOK")
    if str(browser.find_element_by_xpath("//div[7]/input").get_attribute(
            "class")) == "inputError":  # проверяем наличие ворнинга в поле пароля
        print("req pwd alert, OK")
    else:
        print("req pwd alert, NotOK")
    if str(browser.find_element_by_xpath("//div[9]/input").get_attribute(
            "class")) == "inputError":  # проверяем наличие ворнинга в поле подтверждения пароля
        print("req pwdConf alert, OK")
    else:
        print("req pwdConf alert, NotOK")
    if str(browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/label").get_attribute(
            "class")) == "inputError":  # проверяем наличие ворнинга в боксе T&C
        print("req T&C alert, OK")
    else:
        print("req T&C alert, NotOK")


password_confirmation_error()
invalid_email_error()
req_fields_empty()
browser.close()