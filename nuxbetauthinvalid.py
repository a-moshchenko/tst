from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

SITE = "https://dev.nuxbet.com/"  # url сайта, на котором будем проводить тест
EP = r"C:\chromedriver\chromedriver"  # Тут указать путь к файлу драйвера браузера
browser = webdriver.Chrome(executable_path=EP)
RESULTS = ("check, result")
print(RESULTS)


def open(SITE):
    browser.get(SITE)
    browser.set_window_size(1086, 1020)
    sleep(2)


def close():
    # Закрывает окно браузера
    browser.close()


def register_open():
    # открывает форму регистрации
    regi = browser.find_element_by_class_name("regBtn")
    regi.click()
    sleep(3)
    browser.refresh()
    sleep(1)


def password_confirmation_error():
    open(SITE)
    register_open()
    # Вводим пароль и некорректное подтверждение
    password_field = browser.find_element_by_xpath("//div[4]/input")
    password_field.click()
    password_field.send_keys("secretZ1")
    sleep(1)
    password_field.send_keys(Keys.TAB)

    password_confirn_field = browser.find_element_by_xpath("//div[6]/input")
    password_confirn_field.click()
    password_confirn_field.send_keys("secretZ2")
    sleep(1)
    password_confirn_color = password_confirn_field.get_attribute("class")
    if password_confirn_color == "inputError":
        print("confirmation, OK")
    else:
        print("confirmation, NotOK")


def invalid_email_error():
    # Вводим емайл без собаки
    open(SITE)
    register_open()
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("qwertry")
    registration_button = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    if email_field.get_attribute("class") == "inputError":
        print("no at mail, OK")
        sleep(1)
    else:
        print("no at mail, NotOK")
        sleep(1)
    if str(browser.page_source).find("Enter valid email address") > 0:
        print("e-mail errMsg, OK")
    else:
        print("e-mail errMsg, NotOK")

    # Вводим емайл без домена
    open(SITE)
    register_open()
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("qwertry@")
    registration_button = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    if registration_button.get_attribute("class") == "inputError":
        print("no domain mail, OK")
    else:
        print("no domain mail, NotOK")
        sleep(1)

    # Вводим мейл с кириллицей
    open(SITE)
    register_open()
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("почта@домен.сру")
    (browser.find_element_by_xpath("//input[2]")).send_keys("autotestuser1672@mail.com")  # вводим имя пользователя
    (browser.find_element_by_xpath("//div[4]/input")).send_keys("secretZ1")  # вводим пароль
    (browser.find_element_by_xpath("//div[6]/input")).send_keys("secretZ1")  # подтверждаем пароль
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/input[4]")))  # соглашаемся с T&C
    registration_button = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    sleep(1)
    if str(browser.page_source).find("Wrong"):
        print("cyr mail, OK")
    else:
        print("cyr mail, NotOK")
        sleep(1)

    # Вводим мейл с пробелом
    open(SITE)
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
        sleep(1)

    # Вводим ранее зарегистрированный мейл
    open(SITE)
    register_open()
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("autotestuser1672@mail.com")
    (browser.find_element_by_xpath("//input[2]")).send_keys("autotestuser1672@mail.com")  # вводим имя пользователя
    (browser.find_element_by_xpath("//div[4]/input")).send_keys("secretZ1")  # вводим пароль
    (browser.find_element_by_xpath("//div[6]/input")).send_keys("secretZ1")  # подтверждаем пароль
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/input[4]")))  # соглашаемся с T&C
    registration_button = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registration_button.click()
    if str(browser.page_source).find("Username/Email already exist") > 0:
        print("used mail alert, OK")
    else:
        print("used mail alert, OK")
        sleep(1)


def req_fields_empty():
    # Проверка алертов на незаполненых обязательных полях
    open(SITE)
    register_open()
    (browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")).click()  # нажимаем "зарегистрироваться" в форме регистрации
    sleep(1)
    mail_field = browser.find_element_by_xpath("//form/div/div/input")
    # print(mail_field.get_attribute("class"))  # разкомментить если нужно дебажить
    if mail_field.get_attribute("class") == "inputError":  # проверяем наличие ворнинга в поле имейла
        print("req mail alert, OK")
    else:
        print("req mail alert, NotOK")
    if str((browser.find_element_by_xpath("//input[2]")).get_attribute(
            "class")) == "inputError":  # проверяем наличие ворнинга в поле имени пользователя
        print("req name alert, OK")
    else:
        print("req name alert, NotOK")
    if str((browser.find_element_by_xpath("//div[7]/input")).get_attribute(
            "class")) == "inputError":  # проверяем наличие ворнинга в поле пароля
        print("req pwd alert, OK")
    else:
        print("req pwd alert, NotOK")
    if str((browser.find_element_by_xpath("//div[9]/input")).get_attribute(
            "class")) == "inputError":  # проверяем наличие ворнинга в поле подтверждения пароля
        print("req pwdConf alert, OK")
    else:
        print("req pwdConf alert, NotOK")
    if str((browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/label")).get_attribute(
            "class")) == "inputError":  # проверяем наличие ворнинга в боксе T&C
        print("req T&C alert, OK")
    else:
        print("req T&C alert, NotOK")


password_confirmation_error()
invalid_email_error()
req_fields_empty()
