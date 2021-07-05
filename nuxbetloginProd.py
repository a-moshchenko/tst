from time import sleep
from datetime import date
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

browser = webdriver.Chrome(executable_path=Path.cwd()/"driwers"/"chromedriver.exe")
current_date = date.today()
data = current_date.strftime("%d,%m,%Y")
screenshot_path = Path.cwd()/"screenshots"/data
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
logout_dropdown_menu = "/html/body/div/div[2]/div/section[4]/header"
def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception:
        print(f"page open, Error, {Exception}")
        browser.close()

def open():
    browser.get("https://nuxbet.com/")
    browser.set_window_size(1086, 1020)
    wait_for_element(main_page_checkpoint)


def password_vizibility_check():
    # Проверяем отображение пароля при нажатии на глаз
    browser.find_element_by_css_selector(".showPass").click()
    sleep(1)
    password_vizible = str(browser.find_element_by_xpath("(//input[@type='text'])[2]").get_attribute("value"))
    try:
        if password_vizible == config.PASSWORD:
            browser.save_screenshot(str(current_date) + "VisiblePasswordNuxbet.png")
            print("password vizible, OK")
        else:
            print("password vizible, NotOK")
    except Exception:
        print(f"password vizible, Error, {Exception}\n password: {password_vizible}")

def login_positiv_flow():
    open()
    browser.find_element_by_css_selector(".loginBtn").click()

    try:
        browser.find_element_by_css_selector(".formHeader")
        print("auth form, OK")
    except Exception:
        print(f"auth form, NotOK, {Exception}")
    logmail = browser.find_element_by_xpath("//input[@type='text']")
    logmail.send_keys(config.AUTH_NAME_EXIST)
    passwd = browser.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys(config.PASSWORD)
    sleep(1) # слип нужен, чтоб изменения отобразились в браузере
    password_vizibility_check()
    logbtn = browser.find_element_by_css_selector(".btnWrap > .mainBtn")
    logbtn.click()
    sleep(2)
    try:
        uname = browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/span[1]")
        if uname.text == config.AUTH_NAME_EXIST:
            browser.save_screenshot(str(current_date) + "LogedInNuxbet.png")
            print("auth, OK")
            print("main page return, OK")
        else:
            print("NOK, uname: ", uname.text)
    except Exception:
        print(f"auth, NotOK, {Exception}")
    log_out()

def log_out():
    wait_for_element(logout_dropdown_menu)
    print("page loaded")
    try:
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/span[2]").click()
        sleep(1)
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/div[2]/a[7]").click()
    except Exception:
        print(f"loged out, {Exception}")

def login_negative_flow():
    open()
    browser.find_element_by_css_selector(".loginBtn").click()
    try:
        browser.find_element_by_css_selector(".formHeader")
        print("auth form, OK")
    except Exception:
        print(f"auth form, NotOK, {Exception}")
    logmail = browser.find_element_by_xpath("//input[@type='text']") # проверка почты без собаки и незаполненный пароль
    logmail.send_keys("noatmail")
    logbtn = browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div[2]/button")
    logbtn.click()
    sleep(1) # слип нужен чтоб форма обновилась
    if str(logmail.get_attribute("class")) == "inputError":
        print("mail !@, OK")
    else: print("mail !@, NotOK")
    if str(browser.find_element_by_xpath("//input[@type='password']").get_attribute("class")) == "inputError":
        print("no password, OK")
    else:
        print("no password, NotOK")
    if str(browser.page_source).find("Enter valid email address") >0 :
        print("mail error messaage, OK")
    else: print("mail error messaage, OK")
    if str(browser.page_source).find("This field is required") >0 :
        browser.save_screenshot(str(current_date) + "NoEtMailNoPasswordNuxbet.png")
        print("empty field message, OK")
    else: print("empty field messaage, OK")

    logmail = browser.find_element_by_xpath("//input[@type='text']")  # проверка валидной почты с незаполненным паролем
    logmail.send_keys(config.AUTH_NAME_EXIST)
    logbtn = browser.find_element_by_css_selector(".btnWrap > .mainBtn")
    logbtn.click()
    sleep(1)  # слип нужен чтоб форма обновилась
    if str(logmail.get_attribute("class")) != "inputError":
        browser.save_screenshot(str(current_date) + "NoPasswordNuxbet.png")
        print("valid mail, OK")
    else: print("valid mail, NotOK")
    browser.refresh()

    logmail = browser.find_element_by_xpath("//input[@type='text']")  # проверка валидной почты с неверным паролем
    logmail.send_keys(config.AUTH_NAME_EXIST)
    logbtn = browser.find_element_by_xpath("//form/div[2]/button")
    passwd = browser.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys("password")
    logbtn.click()
    sleep(1)  # слип нужен чтоб форма обновилась
    if str(browser.page_source).find("Incorrect login or password. Please check again."):
        browser.save_screenshot(str(current_date) + "WrongPasswordNuxbet.png")
        print("invalid password message, OK")
    else: print("invalid password message, NotOK")
    browser.refresh()

login_positiv_flow()
browser.refresh()
login_negative_flow()
browser.close()


