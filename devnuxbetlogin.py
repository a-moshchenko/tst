from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

EXECUTABLE_PATH = r"C:\chromedriver\chromedriver"  # Тут указать путь к файлу драйвера браузера
browser = webdriver.Chrome(executable_path=EXECUTABLE_PATH)

AUTH_NAME_EXIST = "autotestuser1672@mail.com"

def open():
    site = "https://dev.nuxbet.com/"
    browser.get(site)
    browser.set_window_size(1086, 1020)
    sleep(2)

def close():
    # Закрывает окно браузера
    browser.close()

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
    passwd = browser.find_element_by_xpath("//div[3]/input")
    passwd.send_keys("secretZ1")
    sleep(1)
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


