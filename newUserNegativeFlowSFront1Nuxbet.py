from datetime import date
from time import sleep
import random
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH, options=chrome_options)
current_date = date.today()
data = current_date.strftime("%d,%m,%Y")

def randnum():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for i in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits

user_name = f"autotestuser{randnum()}"

def auth_open():
    sleep(1)
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

def negative_flow_authorization():
    # проверяем пустые поля
    auth_open()
    browser.find_element_by_xpath("//div[6]/button").click()
    if browser.find_element_by_xpath("//input[@type='text']").get_attribute("class") == "inputError":
        print("no username warning, OK")
    else:
        print("no username warning, NotOK")
    if browser.find_element_by_xpath("//input[@type='password']").get_attribute("class") == "inputError":
        print("no password warning, OK")
    else:
        print("no password warning, NotOK")
    if browser.find_element_by_xpath("//input[@type='password']").get_attribute("class") == "inputError":
        print("no password warning, OK")
    else:
        print("no password warning, NotOK")
    if browser.find_element_by_xpath("(//input[@type='password'])[2]").get_attribute("class") == "inputError":
        print("no password comfirmation warning, OK")
    else:
        print("no password confirmation, NotOK")
    if browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/label").get_attribute("class") == "inputError":
        print("no T&C comfirmation warning, OK")
    else:
        print("no T&C confirmation, NotOK")
    browser.save_screenshot(str(f"{current_date}EmptyFieldsSFront1Nuxbet.png"))

    # проверяем без паролей
    open()
    #auth_open()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("autotestuser0000")
    browser.find_element_by_xpath("//div[6]/button").click()
    if browser.find_element_by_xpath("//input[@type='text']").get_attribute("class") != "inputError":
        print("no username warning, OK")
    else:
        print("no username warning, NotOK")
    if browser.find_element_by_xpath("//input[@type='password']").get_attribute("class") == "inputError":
        print("no password warning, OK")
    else:
        print("no password warning, NotOK")
    if browser.find_element_by_xpath("//input[@type='password']").get_attribute("class") == "inputError":
        print("no password warning, OK")
    else:
        print("no password warning, NotOK")
    if browser.find_element_by_xpath("(//input[@type='password'])[2]").get_attribute("class") == "inputError":
        print("no password comfirmation warning, OK")
    else:
        print("no password confirmation, NotOK")
    if browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/label").get_attribute("class") == "inputError":
        print("no T&C comfirmation warning, OK")
    else:
        print("no T&C confirmation, NotOK")
    if str(browser.page_source).find("shortText.field_required") >0  or str(browser.page_source).find("This field is required") >0:
        print("required field message, OK")
    else:
        print("required field message, NotOK")
    browser.save_screenshot(str(current_date)+"EmptyPasswordsSFront1Nuxbet.png")

    # проверяем с неправильным подтверждением пароля
    open()
    #auth_open()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("autotestuser0000")
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("secretZ2")
    browser.find_element_by_css_selector(".passWrap:nth-child(4) > .showPass").click()
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[5]/div").click()
    if browser.find_element_by_xpath("(//input[@type='text'])[3]").get_attribute("class") == "inputError":
        print("wrong password comfirmation warning, OK")
    else:
        print("wrong password confirmation, NotOK")
    browser.save_screenshot(str(current_date) + "WrongPasswordConfirmationSFront1Nuxbet.png")

    # проверяем с нечекнутым T&C боксом
    open()
    #auth_open()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("autotestuser0000")
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("//div[6]/button").click()
    if browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/label").get_attribute("class") == "inputError":
        print("no T&C comfirmation warning, OK")
    else:
        print("no T&C confirmation, NotOK")

    # проверяем киррилицу в поле юзернейм
    open()
    #auth_open()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("юзернейм")
    if browser.find_element_by_xpath("//input[@type='text']").get_attribute("class") == "inputError":
        print("cyrylik username warning, OK")
    else:
        print("cyrylik username warning, NotOK")
    browser.save_screenshot(str(current_date) + "CyrylikUsernameSFront1Nuxbet.png")

    # проверяем ранее зарегистрированный юзернейм
    open()
    #auth_open()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("autotestuser1672")
    browser.find_element_by_xpath("//input[@type='password']").send_keys("secretZ2")
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("secretZ2")
    try:
        terms_checkbox = browser.find_element_by_xpath("//form/div/div/label")
        browser.execute_script("arguments[0].click();", terms_checkbox)
    except:
        print("T&C Error")
    browser.find_element_by_xpath("//div[6]/button").click()
    sleep(1) # нужно чтоб форма обновилась
    if str(browser.page_source).find("Username/Email already exist") >0:
        print("EsistingUser warning, OK")
    else:
        print("EsistingUser warning, NotOK")
    browser.save_screenshot(str(current_date)+"ExistingUsernameSFront1Nuxbet.png")

open()
negative_flow_authorization()
browser.close()