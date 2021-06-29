from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

EXECUTABLE_PATH = r"C:\chromedriver\chromedriver"  # Тут указать путь к файлу драйвера браузера
browser = webdriver.Chrome(executable_path=EXECUTABLE_PATH)
PASSWORD = "secretZ1"
AUTH_NAME_EXIST = "autotestuser1672@mail.com"

def open():
    site = "https://dev.nuxbet.com/"
    browser.get(site)
    browser.set_window_size(1086, 1020)
    sleep(2)

def close():
    # Закрывает окно браузера
    browser.close()

def password_vizibility_check():
    # Проверяем отображение пароля при нажатии на глаз
    browser.find_element_by_xpath("//div[3]/div").click()
    sleep(1)
    password_vizible = str(browser.find_element_by_xpath("//div[3]/input").get_attribute("value"))
    try:
        print(password_vizible)
        if password_vizible == PASSWORD:
            print("password vizible, OK")
        else:
            print("password vizible, NotOK")
    except:
        print("password vizible, Error")
        print(password_vizible)

def login():
    open()
    sleep(2)
    logBtn = browser.find_element_by_xpath("//div[3]/a")
    logBtn.click()
    try:
        browser.find_element_by_css_selector(".formHeader")
        print("auth form, OK")
    except:
        print("auth form, NotOK")
    logmail = browser.find_element_by_xpath("//input[@type='text']")
    logmail.send_keys("autotestuser1672@mail.com")
    passwd = browser.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys(PASSWORD)
    sleep(1)
    password_vizibility_check()
    logbtn = browser.find_element_by_xpath("//form/div[2]/button")
    logbtn.click()
    sleep(2)
    try:
        uname = browser.find_element_by_xpath("//div[2]/div[3]")
        if uname.text == AUTH_NAME_EXIST:
            print("auth, OK")
            print("main page return, OK")
        else:
            print("NOK, uname: ", uname.text)
    except:
        print("auth, NotOK")

login()


