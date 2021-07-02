from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH)
current_date = date.today()
data = current_date.strftime("%d,%m,%Y")

def open():
    browser.get(config.SITE)
    browser.set_window_size(1086, 1020)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/section[2]/div"))
        )
    except:
        print("page open, Error")
        browser.close()

def password_vizibility_check():
    # Проверяем отображение пароля при нажатии на глаз
    browser.find_element_by_xpath("//div[3]/div").click()
    sleep(1)
    password_vizible = str(browser.find_element_by_xpath("//div[3]/input").get_attribute("value"))
    try:
        if password_vizible == config.PASSWORD:
            browser.save_screenshot(str(data) + "VisiblrPasswordDevNuxbet.png")
            print("password vizible, OK")
        else:
            print("password vizible, NotOK")
    except:
        print("password vizible, Error")
        print(password_vizible)

def login_positiv_flow():
    open()
    browser.find_element_by_xpath("//div[3]/a").click()

    try:
        browser.find_element_by_css_selector(".formHeader")
        print("auth form, OK")
    except:
        print("auth form, NotOK")
    logmail = browser.find_element_by_xpath("//input[@type='text']")
    logmail.send_keys(config.AUTH_NAME_EXIST)
    passwd = browser.find_element_by_xpath("//input[@type='password']")
    passwd.send_keys(config.PASSWORD)
    sleep(1) # слип нужен, чтоб изменения отобразились в браузере
    password_vizibility_check()
    logbtn = browser.find_element_by_xpath("//form/div[2]/button")
    logbtn.click()
    sleep(2)
    try:
        uname = browser.find_element_by_xpath("//div[2]/div[3]")
        if uname.text == config.AUTH_NAME_EXIST:
            print("authorisation, OK")
            print("main page return, OK")
            browser.save_screenshot(str(data) + "UserLogedInDevNuxbet.png")
        else:
            print("NOK, uname: ", uname.text)
    except:
        print("authorisation, NotOK")
    log_out()

def log_out():
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/section[4]/header"))
        )
    except:
        print("page open, Error")
        browser.close()
    print("page loaded")
    try:
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/span[2]").click()
        sleep(1)
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/div[2]/a[7]").click()
    except:
        print("loged out")

def login_negative_flow():
    open()
    browser.find_element_by_xpath("//div[3]/a").click()
    try:
        browser.find_element_by_css_selector(".formHeader")
        print("authorisation form, OK")
    except:
        print("authorisation form, NotOK")
    login_mail = browser.find_element_by_xpath("//input[@type='text']") # проверка почты без собаки и незаполненный пароль
    login_mail.send_keys("noatmail")
    login_button = browser.find_element_by_xpath("//form/div[2]/button")
    login_button.click()
    sleep(1) # слип нужен чтоб форма обновилась
    if str(login_mail.get_attribute("class")) == "inputError":
        browser.save_screenshot(str(data) + "NoEtMailLoginDevNuxbet.png")
        print("mail without et, OK")
    else:
        print("mail without et, NotOK")
    if str(browser.find_element_by_xpath("//div[1]/div[4]/input").get_attribute("class")) == "inputError":
        print("no password, OK")
    else:
        print("no password, NotOK")
    if str(browser.page_source).find("Enter valid email address") > 0 :
        print("mail error messaage, OK")
    else:
        print("mail error messaage, OK")
    if str(browser.page_source).find("This field is required") > 0 :
        print("empty field message, OK")
    else:
        print("empty field messaage, OK")

    login_mail = browser.find_element_by_xpath("//input[@type='text']")  # проверка валидной почты с незаполненным паролем
    login_mail.send_keys(config.AUTH_NAME_EXIST)
    login_button = browser.find_element_by_xpath("//form/div[2]/button")
    login_button.click()
    sleep(1)  # слип нужен чтоб форма обновилась
    if str(login_mail.get_attribute("class")) != "inputError":
        browser.save_screenshot(str(f"{data}NoMailDevNuxbet.png"))
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
    if str(browser.page_source).find("Incorrect login or password. Please check again."):
        browser.save_screenshot(str(f"{data}WrongPasswordLoginPasswordDevNuxbet.png"))
        print("invalid password message, OK")
    else:
        print("invalid password message, NotOK")
    browser.refresh()

login_positiv_flow()
browser.refresh()
login_negative_flow()
browser.close()