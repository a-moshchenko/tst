from time import sleep
import random
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH, options=chrome_options)
browser.set_window_size(1086, 1020)
current_date = date.today()
data = current_date.strftime("%d,%m,%Y")
screenshot_path = config.SCREENSHOTPATHAUTH
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
authorization_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"


def random_four_digits_number():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for i in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits


user_name = "autotestuser" + random_four_digits_number()


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"page open, Error, {e}")
        browser.close()


def open_main_page():
    browser.get(config.SFRONT1SITE)
    wait_for_element(main_page_checkpoint)
    browser.refresh()


def authorisation_form_open():
    browser.find_element_by_css_selector(".regBtn").click()
    wait_for_element(authorization_form_checkpoint)
    browser.refresh()
    wait_for_element(authorization_form_checkpoint)
    try:
        browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
        sleep(1)
        browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
        print("login-registration swap, OK")
    except Exception as e:
        print(f"login-registration swap, NotOK, {e}")


def fill_fields():
    try:
        browser.find_element_by_xpath("//input[@type='text']").send_keys(user_name)
    except Exception as e:
        print(f"username input Error, {e}")
    try:
        browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    except Exception as e:
        print(f"password input Error, {e}")
    try:
        browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(config.PASSWORD)
    except Exception as e:
        print(f"password confirmation input error, {e}")
    try:
        terms_checkbox = browser.find_element_by_xpath("//form/div/div/label")
        browser.execute_script("arguments[0].click();", terms_checkbox)
    except Exception as e:
        print(f"T&C Error, {e}")
    password_visibility()


def password_visibility():
    try:
        browser.find_element_by_css_selector(".passWrap:nth-child(4) > .showPass").click()
        browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[5]/div").click()
    except Exception as e:
        print(f"password vizibility Error, {e}")
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
    open_main_page()
    try:
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/span[1]").click()
        sleep(1)  # ждем появления дропдакн меню
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/div[2]/a[7]").click()
        open_main_page()
    except Exception as e:
        print(f"log out Error, {e}")
        browser.close()
    print("loged out")


open_main_page()
authorisation_form_open()
fill_fields()
browser.save_screenshot(f"{screenshot_path}SFront1Nuxbet.png")
print(f"Username: {user_name}\nPassword: {config.PASSWORD}")
sleep(2)
browser.find_element_by_xpath("//div[6]/button").click()
sleep(1)
if browser.page_source.find(user_name) > 0:
    print("registration, OK")
else:
    print("registration, NotOK")
log_out()
browser.close()
