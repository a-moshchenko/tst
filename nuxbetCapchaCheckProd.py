from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

EXECUTABLE_PATH = r"C:\chromedriver\chromedriver"  # Тут указать путь к файлу драйвера браузера
browser = webdriver.Chrome(executable_path=EXECUTABLE_PATH)

def open():
    browser.get("https://nuxbet.com/")
    browser.set_window_size(1086, 1020)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/section[4]/header"))
        )
    except:
        print("page open, Error")
        browser.close()

def login_opn():
    login_btn_main = browser.find_element_by_class_name("regBtn")
    login_btn_main.click()

def general_run():
    open()
    login_opn()
    sleep(1)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(
        config.AUTHNAME)  # вводим мейл пользователя
    #browser.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(
    #    "LoremIpsum")  # вводим имя пользователя
    browser.find_element_by_xpath("//input[@type='password']").send_keys(
        config.PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(
        config.PASSWORD)  # подтверждаем пароль
    TC = browser.find_element_by_xpath(
        "//form/div/div/label")  # определяем элемент чeкбокс terms&conditions
    browser.execute_script("arguments[0].click();", TC)  # соглашаемся с T&C
    for i in range(12):
        sleep(2)
        try:
            login_button = browser.find_element_by_xpath(
                "//div[7]/button")
            login_button.click()
        except:
            print("Capcha, OK")
            break


general_run()
browser.close()
