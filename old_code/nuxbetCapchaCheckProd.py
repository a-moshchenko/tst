from time import sleep
from selenium.common.exceptions import NoSuchElementException
import commonFunctions
import config

browser = commonFunctions.browser
screenshot_path = config.SCREENSHOT_PATH_AUTHORISATION
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"


def login_form_open():
    login_button_main = browser.find_element_by_class_name("regBtn")
    login_button_main.click()


def general_run():
    commonFunctions.open_page(config.SITE_PROD, main_page_checkpoint)
    login_form_open()
    sleep(1)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(
        config.AUTHORISATION_NAME)  # вводим мейл пользователя
    browser.find_element_by_xpath("//input[@type='password']").send_keys(
        config.PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(
        config.PASSWORD)  # подтверждаем пароль
    terms_and_conditions = browser.find_element_by_xpath(
        "//form/div/div/label")  # определяем элемент чeкбокс terms&conditions
    browser.execute_script("arguments[0].click();", terms_and_conditions)  # соглашаемся с T&C
    for iterable_element_of_sequence_of_numbers_created_by_range in range(12):
        sleep(2)
        try:
            login_button = browser.find_element_by_xpath(
                "//div[7]/button")
            login_button.click()
        except NoSuchElementException:
            browser.save_screenshot(f"{screenshot_path}CapchaNuxbet.png")
            print(f"Capcha, OK")
            break


general_run()
browser.close()
