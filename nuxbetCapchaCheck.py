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
data = current_date.strftime("%d,%m,%Y")
screenshot_path = config.SCREENSHOTPATHAUTH
main_page_checkpoint = "/html/body/div/div[2]/div/section[4]/header"



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


def login_opn():
    login_button_main = browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/button")
    login_button_main.click()


def general_run():
    open_main_page()
    login_opn()
    sleep(1)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(
        config.AUTHNAME)  # вводим мейл пользователя
    browser.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(
        "LoremIpsum")  # вводим имя пользователя
    browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[4]/input").send_keys(
        config.PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[6]/input").send_keys(
        config.PASSWORD)  # подтверждаем пароль
    terms_and_conditions = browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/input[4]")  # определяем элемент чкубокс terms&conditions
    browser.execute_script("arguments[0].click();", terms_and_conditions)  # соглашаемся с T&C
    for i in range(12):
        sleep(2)
        try:
            login_button = browser.find_element_by_xpath(
                "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
            login_button.click()
        except Exception:  # ексепшн является ожидаемым результатом, поэтому не описан
            print(f"Capcha, OK")
            browser.save_screenshot(f"{screenshot_path}Capchadevnuxbet.png")
            break


general_run()
browser.close()
