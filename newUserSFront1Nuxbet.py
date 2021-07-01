from datetime import date
from time import sleep
import random
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH, chrome_options=chrome_options)
current_date = date.today()
data = current_date.strftime("%d,%m,%Y")

def randnum():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for i in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits

user_name = "autotestuser" + randnum()

def open():
    browser.get("https://sfront1.nuxbet.com/")
    browser.set_window_size(1086, 1020)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/section[2]/div"))
        )
    except:
        print("page open, Error")
        browser.close()
    browser.refresh()

def auth_open():
    browser.find_element_by_css_selector(".regBtn").click()
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div[2]/div/div/div/div"))
        )
    except:
        print("registr form open, Error")
        browser.close()
    browser.refresh()
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div[2]/div/div/div/div"))
        )
    except:
        print("registr form open, Error")
        browser.close()
    try:
        browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
        sleep(1)
        browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
        print("login-registration swap, OK")
    except:
        print("login-registration swap, NotOK")

def fill_fields():
    try:
        browser.find_element_by_xpath("//input[@type='text']").send_keys(user_name)
    except:
        print("username input Error")
    try:
        browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    except:
        print("password input Error")
    try:
        browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(config.PASSWORD)
    except:
        print("password confirmation input error")
    try:
        terms_checkbox = browser.find_element_by_xpath("//form/div/div/label")
        browser.execute_script("arguments[0].click();", terms_checkbox)
    except:
        print("T&C Error")
    password_vizibility()

def password_vizibility():
    try:
        browser.find_element_by_css_selector(".passWrap:nth-child(4) > .showPass").click()
        browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[5]/div").click()
    except:
        print("password vizibility Error")
    if browser.find_element_by_xpath("(//input[@type='text'])[2]").get_attribute("value") == config.PASSWORD:
        print("password vizibility, OK")
    else:
        print("password vizibility, NotOK")
    if browser.find_element_by_xpath("(//input[@type='text'])[3]").get_attribute("value") == config.PASSWORD:
        print("password confirmation visibility, OK")
    else:
        print("password confirmation visibility, NotOK")

def log_out():
    open()
    try:
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/span[1]").click()
        sleep(1) # ждем появления дропдакн меню
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/div[2]/a[7]").click()
        open()
    except:
        print("log out Error")
        browser.close()
    print("loged out")

open()
auth_open()
fill_fields()
browser.save_screenshot(str(current_date)+"PozitiveRegistrationSFront1Nuxbet.png")
print("Username: ", user_name)
print("Password: ", config.PASSWORD)
sleep(2)
browser.find_element_by_xpath("//div[6]/button").click()
sleep(1)
if str(browser.page_source).find(user_name)>0:
    print("registration, OK")
else:
    print("registration, NotOK")
log_out()
browser.close()