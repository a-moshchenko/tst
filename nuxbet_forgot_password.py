from time import sleep
import random
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

def login():
    open()
    login_button = browser.find_element_by_xpath("//div[3]/a")
    login_button.click()
    try:
        browser.find_element_by_css_selector(".formHeader")
        print("auth form, OK")
    except:
        print("auth form, NotOK")
    forgot_password_button = browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div[1]/div[2]/div[2]")
    forgot_password_button.click()
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div[2]/div/div/div/div"))
        )
    except:
        print("forgot password, Error")
        browser.close()
    print("forgot password form, OK")

    send_button = browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div[2]")
    send_button.click()
    sleep(1) # слип нужен чтоб дать форме обновиться


    if str(browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/input").get_attribute("class")) == "inputError":
        print("no email, OK")
    else:
        print("no email, NotOK")

    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/nav/div/a[2]"))
        )
    except:
        print()
login()