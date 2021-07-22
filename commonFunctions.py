from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")
#chrome_options.add_argument("headless")

browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH, options=chrome_options)


def open_page(page_url, page_checkpoint):
    browser.get(page_url)
    wait_for_element(page_checkpoint)
    sleep(1)


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"wait for element, Error, {e}, {xpath}")
        browser.close()


def register_open(form_checkpoint):
    # открывает форму регистрации
    registration_button = browser.find_element_by_class_name("regBtn")
    registration_button.click()
    sleep(1)  # без этого слипа работает только в дебаге)
    wait_for_element(form_checkpoint)
    browser.refresh()
    wait_for_element(form_checkpoint)


def capcha_finder():
    sleep(1)
    source = browser.page_source
    if str(source).find("Some problems with captcha") > 0:
        print("Error! Capcha found! Turn off capcha and rerun")
        return False
    else:
        return True
