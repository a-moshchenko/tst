from time import sleep
import random
from datetime import date
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
browser = webdriver.Chrome(executable_path=Path.cwd()/"driwers"/"chromedriver.exe", options=chrome_options)
current_date = date.today()
data = current_date.strftime("%d,%m,%Y")
screenshot_path = Path.cwd()/"screenshots"/data
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
authrization_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"

def randnum():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for i in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits

user_name = "autotestuser" + randnum()

def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception:
        print(f"page open, Error, {Exception}")
        browser.close()

def open():
    browser.get("https://sfront1.nuxbet.com/")
    browser.set_window_size(1086, 1020)
    wait_for_element(main_page_checkpoint)
    browser.refresh()

def auth_open():
    browser.find_element_by_css_selector(".regBtn").click()
    wait_for_element(authrization_form_checkpoint)
    browser.refresh()
    wait_for_element(authrization_form_checkpoint)
    try:
        browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
        sleep(1)
        browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
        print("login-registration swap, OK")
    except Exception:
        print(f"login-registration swap, NotOK, {Exception}")

def fill_fields():
    try:
        browser.find_element_by_xpath("//input[@type='text']").send_keys(user_name)
    except Exception:
        print(f"username input Error, {Exception}")
    try:
        browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    except Exception:
        print(f"password input Error, {Exception}")
    try:
        browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(config.PASSWORD)
    except Exception:
        print(f"password confirmation input error, {Exception}")
    try:
        terms_checkbox = browser.find_element_by_xpath("//form/div/div/label")
        browser.execute_script("arguments[0].click();", terms_checkbox)
    except Exception:
        print(f"T&C Error, {Exception}")
    password_vizibility()

def password_vizibility():
    try:
        browser.find_element_by_css_selector(".passWrap:nth-child(4) > .showPass").click()
        browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[5]/div").click()
    except Exception:
        print(f"password vizibility Error, {Exception}")
    if browser.find_element_by_xpath("(//input[@type='text'])[2]").get_attribute("value") == config.PASSWORD:
        print("password vizibility, OK")
    else:
        print("password vizibility, NotOK")
    if browser.find_element_by_xpath("(//input[@type='text'])[3]").get_attribute("value") == config.PASSWORD:
        browser.save_screenshot(f"{screenshot_path}VisiblePasswordSFront1Nuxbet.png")
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
    except Exception:
        print(f"log out Error, {Exception}")
        browser.close()
    print("loged out")

open()
auth_open()
fill_fields()
browser.save_screenshot(str(f"{screenshot_path}SFront1Nuxbet.png"))
print(f"Username: {user_name}\nPassword: {config.PASSWORD}")
sleep(2)
browser.find_element_by_xpath("//div[6]/button").click()
sleep(1)
if str(browser.page_source).find(user_name)>0:
    print("registration, OK")
else:
    print("registration, NotOK")
log_out()
browser.close()