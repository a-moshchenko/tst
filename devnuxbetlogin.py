from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config

browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH)
browser.set_window_size(1086, 1020)
current_date = date.today()
date = current_date.strftime("%d,%m,%Y")
screenshot_path = config.SCREENSHOTPATHAUTH
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
logout_form_checkpoint = "/html/body/div/div[2]/div/section[4]/header"


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"page open, Error, {e}")
        browser.close()


def open_main_page():
    browser.get(config.SITE)
    wait_for_element(main_page_checkpoint)


def password_visibility_check():
    # Проверяем отображение пароля при нажатии на глаз
    browser.find_element_by_xpath("//div[3]/div").click()
    sleep(1)
    password_visible = str(browser.find_element_by_xpath("//div[3]/input").get_attribute("value"))
    try:
        if password_visible == config.PASSWORD:
            browser.save_screenshot(f"{screenshot_path}VisiblrPasswordDevNuxbet.png")
            print("password visible, OK")
        else:
            print("password visible, NotOK")
    except Exception as e:
        print(f"password visible, Error, {e}\n{password_visible}")


def login_positive_flow():
    open_main_page()
    browser.find_element_by_xpath("//div[3]/a").click()

    try:
        browser.find_element_by_css_selector(".formHeader")
        print("auth form, OK")
    except Exception as e:
        print(f"auth form, NotOK, Error {e}")
    logmail = browser.find_element_by_xpath("//input[@type='text']")
    logmail.send_keys(config.AUTH_NAME_EXIST)
    passwd = browser.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys(config.PASSWORD)
    sleep(1)  # слип нужен, чтоб изменения отобразились в браузере
    password_visibility_check()
    logbtn = browser.find_element_by_xpath("//form/div[2]/button")
    logbtn.click()
    sleep(2)
    try:
        uname = browser.find_element_by_xpath("//div[2]/div[3]")
        if uname.text == config.AUTH_NAME_EXIST:
            print("authorisation, OK\n main page return, OK")
            browser.save_screenshot(f"{screenshot_path}UserLogedInDevNuxbet.png")
        else:
            print(f"NOK, uname: {uname.text}")
    except Exception as e:
        print(f"authorisation, NotOK, {e}")
    log_out()


def log_out():
    wait_for_element(logout_form_checkpoint)
    print("page loaded")
    try:
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/span[2]").click()
        sleep(1)
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/div[2]/a[7]").click()
    except Exception as e:  # ексепшн является частью позитив флоу
        print(f"loged out, {e}")


def login_negative_flow():
    open_main_page()
    browser.find_element_by_xpath("//div[3]/a").click()
    try:
        browser.find_element_by_css_selector(".formHeader")
        print("authorisation form, OK")
    except Exception as e:
        print(f"authorisation form, NotOK, {e}")
    login_mail = browser.find_element_by_xpath("//input[@type='text']")  # проверка почты без собаки и без пароля
    login_mail.send_keys("noatmail")
    login_button = browser.find_element_by_xpath("//form/div[2]/button")
    login_button.click()
    sleep(1)  # слип нужен чтоб форма обновилась
    if login_mail.get_attribute("class") == "inputError":
        browser.save_screenshot(f"{screenshot_path}NoEtMailLoginDevNuxbet.png")
        print("mail without et, OK")
    else:
        print("mail without et, NotOK")
    if browser.find_element_by_xpath("//div[1]/div[4]/input").get_attribute("class") == "inputError":
        print("no password, OK")
    else:
        print("no password, NotOK")
    if browser.page_source.find("Enter valid email address") > 0:
        print("mail error message, OK")
    else:
        print("mail error message, NotOK")
    if browser.page_source.find("This field is required") > 0:
        print("empty field message, OK")
    else:
        print("empty field message, NotOK")

    login_mail = browser.find_element_by_xpath("//input[@type='text']")  # проверка почты с незаполненным паролем
    login_mail.send_keys(config.AUTH_NAME_EXIST)
    login_button = browser.find_element_by_xpath("//form/div[2]/button")
    login_button.click()
    sleep(1)  # слип нужен чтоб форма обновилась
    if login_mail.get_attribute("class") != "inputError":
        browser.save_screenshot(f"{screenshot_path}NoMailDevNuxbet.png")
        print("valid mail, OK")
    else:
        print("valid mail, NotOK")
    browser.refresh()

    login_mail = browser.find_element_by_xpath("//input[@type='text']")  # проверка валидной почты с неверным паролем
    login_mail.send_keys(config.AUTH_NAME_EXIST)
    login_button = browser.find_element_by_xpath("//form/div[2]/button")
    password = browser.find_element_by_xpath("//input[@type='password']")
    password.send_keys("password")
    login_button.click()
    sleep(1)  # слип нужен чтоб форма обновилась
    if browser.page_source.find("Incorrect login or password. Please check again."):
        browser.save_screenshot(f"{screenshot_path}WrongPasswordLoginPasswordDevNuxbet.png")
        print("invalid password message, OK")
    else:
        print("invalid password message, NotOK")
    browser.refresh()


login_positive_flow()
browser.refresh()
login_negative_flow()
browser.close()
