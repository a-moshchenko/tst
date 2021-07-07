from time import sleep
from datetime import date
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import config

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

browser = webdriver.Chrome(executable_path=Path.cwd()/"driwers"/"chromedriver.exe", options=chrome_options)
current_date = date.today()
date = current_date.strftime("%d,%m,%Y")
screenshot_path = Path.cwd()/"screenshots"/date
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
registration_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"registration form open, Error, {e}")
        browser.close()


def open_main_page():
    browser.get(config.SFRONT3SITE)
    browser.set_window_size(1086, 1020)
    wait_for_element(main_page_checkpoint)
    sleep(1)


def open_registration_form():
    browser.find_element_by_css_selector(".mainBtn").click()
    wait_for_element(registration_form_checkpoint)
    browser.refresh()
    wait_for_element(registration_form_checkpoint)


def to_login_form_and_back():
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
    sleep(1)
    try:
        browser.find_element_by_xpath("//div[@class='formWrap authForm']")
        print("swich to login form, OK")
        browser.find_element_by_xpath("//div[2]/span[2]").click()
    except Exception as e:
        print(f"swich to login form, NotOK, Error, {e}")
    try:
        wait_for_element("//div[@class='formWrap authForm']")
        print("swich to registration form, OK")
    except Exception as e:
        print(f"swich to registration form, NotOK, Error, {e}")


def empty_fields_check():
    open_registration_form()
    browser.find_element_by_xpath("//div[@class='mainBtn']").click()


open_main_page()
open_registration_form()
to_login_form_and_back()
