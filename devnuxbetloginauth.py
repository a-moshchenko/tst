from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

ep = r"C:\chromedriver\chromedriver" # Тут указать путь к файлу драйвера браузера
browser = webdriver.Chrome(executable_path=ep)
results = ("check, result")
print(results)
def randnum():
    #генерит рандомную строку из четырех цыфр
    a = ""
    for i in range (4):
        a += str(random.randint(1,9))
    return a
uname = "autotestuser" + randnum()

def finalChecks():
    # Проверяет имя пользователя в форме регистрации
    print("userMail, OK")
    print("userName, OK")
    if browser.find_element_by_xpath("//div[4]/input").get_attribute("value") == "secretZ1":
        print("password visibility, OK")
    else:
        print("password visibility, NotOK")
    if browser.find_element_by_xpath("//div[6]/input").get_attribute("value") == "secretZ1":
        print("passwordCon visibility, OK")
    else:
        print("passwordCon visibility, NotOK")




def open():
    site = "https://dev.nuxbet.com/"
    browser.get(site)
    browser.set_window_size(1086, 1020)
    sleep(2)

def close():
    # Закрывает окно браузера
    browser.close()

def registrValid():
    # Выполняет регистрацию пользователя по позитив флоу с валидными даными
    regi = browser.find_element_by_class_name("regBtn")
    regi.click()
    sleep(1)
    try:
        # Проверяем наличие формы авторизации
        browser.find_element_by_class_name("authForm")
        print("authForm, OK")
    except:
        # если формы нет - закрываем окно браузера и выводим ерор
        print("authForm, NoPopUp")
        close()
    try:
        # Вводим емайл
        emailInput = browser.find_element_by_xpath("//form/div/div/input")
        emailInput.click()
        emailInput.send_keys(str(uname+ "@mail.com"))
    except:
        print("E-mail input, ERROR")

    try:
        # Вводим юзернейм
        userLogin = browser.find_element_by_xpath("//input[2]")
        userLogin.click()
        userLogin.send_keys(uname)
    except:
        print("login input, ERROR")
    try:
        # Вводим пароль и подтверждение
        pwd = browser.find_element_by_xpath("//div[4]/input")
        pwd.click()
        pwd.send_keys("secretZ1")
        sleep(1)
        pwd.send_keys(Keys.TAB)

        pwdConfirm = browser.find_element_by_xpath("//div[6]/input")
        pwdConfirm.click()
        pwdConfirm.send_keys("secretZ1")

        try:
            # Проверяем нескрытое отображение пароля
            showPwd = browser.find_element_by_xpath("//div[4]/div")
            showPwd.click()
            showPwdConf = browser.find_element_by_xpath("//div[6]/div")
            showPwdConf.click()
            sleep(1)

        except:
            print("Visible password ERROR")
    except:
        print("Password input Error")

    try:
        refCode = browser.find_element_by_xpath("//div/input[3]")
        refCode.send_keys("QwERty123!@#")
        sleep(1)
        if refCode.get_attribute("value") == "QwERty123!@#":
            print("ref code, OK")
        else:
            print("refCode: ", refCode.get_attribute("value"))
    except:
        print("ref code, NotOK")
    try:
        # Соглашаемся с T&C
        tc = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/input[4]")
        browser.execute_script("arguments[0].click();", tc)
        print("T&C acepted, OK")
    except:
        print("T&C ERROR")


    finalChecks()
    registerBtn = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
    registerBtn.click()

    sleep(2)

    user = browser.find_element_by_xpath("//div[2]/div[3]")
    if user.text == str(uname + "@mail.com"):
        print("main page return, OK")
    else:
        print("main page return, NotOK")



    print("Username: ", uname)
    print("Usermail: ", uname, "@mail.com")








open()
try:
    registrValid()
except:
    print("registration, registration Error")
