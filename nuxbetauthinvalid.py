from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

ep = r"C:\chromedriver\chromedriver"  # Тут указать путь к файлу драйвера браузера
browser = webdriver.Chrome(executable_path=ep)
results = ("check, result")
print(results)

def open():
    site = "https://dev.nuxbet.com/"
    browser.get(site)
    browser.set_window_size(1086, 1020)
    sleep(2)

def close():
    # Закрывает окно браузера
    browser.close()

def registrOpen():
    # открывает форму регистрации
    regi = browser.find_element_by_class_name("regBtn")
    regi.click()
    sleep(3)
    browser.refresh()
    sleep(1)

def passwordConfirmationError():
    open()
    registrOpen()
    # Вводим пароль и некорректное подтверждение
    pwd = browser.find_element_by_xpath("//div[4]/input")
    pwd.click()
    pwd.send_keys("secretZ1")
    sleep(1)
    pwd.send_keys(Keys.TAB)

    pwdConfirm = browser.find_element_by_xpath("//div[6]/input")
    pwdConfirm.click()
    pwdConfirm.send_keys("secretZ2")
    sleep(1)
    pasConColor = pwdConfirm.get_attribute("class")
    if pasConColor == "inputError":
        print("confirmation, OK")
    else:
        print("confirmation, NotOK")


def invalidEmailError():
    # Вводим емайл без собаки
    open()
    registrOpen()
    emailInput = browser.find_element_by_xpath("//form/div/div/input")
    emailInput.click()
    emailInput.send_keys("qwertry")
    registerBtn = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registerBtn.click()
    if emailInput.get_attribute("class") == "inputError":
        print("no at mail, OK")
        sleep(1)
    else:
        print("no at mail, NotOK")
        sleep(1)
    if str(browser.page_source).find("Enter valid email address") >0:
        print("e-mail errMsg, OK")
    else:
        print("e-mail errMsg, NotOK")


    # Вводим емайл без домена
    open()
    registrOpen()
    emailInput = browser.find_element_by_xpath("//form/div/div/input")
    emailInput.click()
    emailInput.send_keys("qwertry@")
    registerBtn = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registerBtn.click()
    if emailInput.get_attribute("class") == "inputError":
        print("no domain mail, OK")
    else:
        print("no domain mail, NotOK")
        sleep(1)

    # Вводим мейл с кириллицей
    open()
    registrOpen()
    emailInput = browser.find_element_by_xpath("//form/div/div/input")
    emailInput.click()
    emailInput.send_keys("почта@домен.сру")
    (browser.find_element_by_xpath("//input[2]")).send_keys("autotestuser1672@mail.com")
    (browser.find_element_by_xpath("//div[4]/input")).send_keys("secretZ1")
    (browser.find_element_by_xpath("//div[6]/input")).send_keys("secretZ1")
    browser.execute_script("arguments[0].click();", (
    browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/input[4]")))
    registerBtn = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registerBtn.click()
    sleep(1)
    if str(browser.page_source).find("Wrong"):
        print("cyr mail, OK")
    else:
        print("cyr mail, NotOK")
        sleep(1)

    # Вводим мейл с пробелом
    open()
    registrOpen()
    emailInput = browser.find_element_by_xpath("//form/div/div/input")
    emailInput.click()
    emailInput.send_keys('"space mail"@mail.u')
    registerBtn = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registerBtn.click()
    if emailInput.get_attribute("class") == "inputError":
        print("space domain, OK")
    else:
        print("space domain, NotOK")
        sleep(1)

    # Вводим ранее зарегистрированный мейл
    open()
    registrOpen()
    emailInput = browser.find_element_by_xpath("//form/div/div/input")
    emailInput.click()
    emailInput.send_keys("autotestuser1672@mail.com")
    (browser.find_element_by_xpath("//input[2]")).send_keys("autotestuser1672@mail.com")
    (browser.find_element_by_xpath("//div[4]/input")).send_keys("secretZ1")
    (browser.find_element_by_xpath("//div[6]/input")).send_keys("secretZ1")
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/input[4]")))
    registerBtn = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registerBtn.click()
    if str(browser.page_source).find("Username/Email already exist") >0:
        print("used mail alert, OK")
    else:
        print("used mail alert, OK")
        sleep(1)

def reqFieldsEmpty():
    # Проверка алертов на незаполненыз обязательных полях
    open()
    registrOpen()
    (browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")).click()
    sleep(1)
    mail = browser.find_element_by_xpath("//form/div/div/input")
    #print(mail.get_attribute("class"))
    if mail.get_attribute("class") == "inputError":
        print("req mail alert, OK")
    else:
        print("req mail alert, NotOK")
    if str((browser.find_element_by_xpath("//input[2]")).get_attribute("class")) == "inputError":
        print("req name alert, OK")
    else:
        print("req name alert, NotOK")
    if str((browser.find_element_by_xpath("//div[7]/input")).get_attribute("class")) == "inputError":
        print("req pwd alert, OK")
    else:
        print("req pwd alert, NotOK")
    if str((browser.find_element_by_xpath("//div[9]/input")).get_attribute("class")) == "inputError":
        print("req pwdConf alert, OK")
    else:
        print("req pwdConf alert, NotOK")
    if str((browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/label")).get_attribute("class")) == "inputError":
        print("req T&C alert, OK")
    else:
        print("req T&C alert, NotOK")






#passwordConfirmationError()
#invalidEmailError()
reqFieldsEmpty()


