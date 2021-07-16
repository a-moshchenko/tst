from time import sleep
from selenium import webdriver
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config

browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH)
current_date = date.today()
date = current_date.strftime("%d,%m,%Y")
screenshot_path = config.SCREENSHOTPATHAUTH


def open_main_page():
    browser.get("https://nuxbet.com/")
    browser.set_window_size(1086, 1020)
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/section[2]/div"))
        )
    except Exception as e:
        print(f"page open, Error, {e}")
        browser.close()


def login_form_open():
    login_btn_main = browser.find_element_by_class_name("regBtn")
    login_btn_main.click()


def general_run():
    open_main_page()
    login_form_open()
    sleep(1)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(
        config.AUTHNAME)  # вводим мейл пользователя
    browser.find_element_by_xpath("//input[@type='password']").send_keys(
        config.PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(
        config.PASSWORD)  # подтверждаем пароль
    terms_and_conditions = browser.find_element_by_xpath(
        "//form/div/div/label")  # определяем элемент чeкбокс terms&conditions
    browser.execute_script("arguments[0].click();", terms_and_conditions)  # соглашаемся с T&C
    for i in range(12):
        sleep(2)
        try:
            login_button = browser.find_element_by_xpath(
                "//div[7]/button")
            login_button.click()
        except Exception:
            browser.save_screenshot(f"{screenshot_path}CapchaNuxbet.png")
            print("Capcha, OK")
            break


general_run()
browser.close()
