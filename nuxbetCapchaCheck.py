from time import sleep
from selenium.common.exceptions import NoSuchElementException
import commonFunctions
import config

browser = commonFunctions.browser
screenshot_path = config.SCREENSHOT_PATH_AUTHORISATION
main_page_checkpoint = "/html/body/div/div[2]/div/section[4]/header"


def open_main_page():
    browser.get(config.SITE)
    commonFunctions.wait_for_element(main_page_checkpoint)


def login_opn():
    login_button_main = browser.find_element_by_xpath("//a[@class='loginBtn']")
    login_button_main.click()


def general_run():
    commonFunctions.open_page(config.SITE, main_page_checkpoint)
    login_opn()
    sleep(1)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(
        config.AUTHORISATION_NAME)  # вводим мейл пользователя
    """  # Эти действия используются для проверуи капчи на форме авторизации
    browser.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(
        "LoremIpsum")  # вводим имя пользователя
    """
    browser.find_element_by_xpath("//input[@type='password']").send_keys(
        config.PASSWORD[1:])  # вводим пароль
    """
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(
        config.PASSWORD)  # подтверждаем пароль
    terms_and_conditions = browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/input[4]")  # определяем элемент чкубокс terms&conditions
    browser.execute_script("arguments[0].click();", terms_and_conditions)  # соглашаемся с T&C
    """
    for iterable_element_in_sequence_of_numbers_created_by_range in range(12):
        sleep(2)
        try:
            login_button = browser.find_element_by_xpath(
                "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
            login_button.click()
        except NoSuchElementException:
            print(f"Capcha, OK")
            browser.save_screenshot(f"{screenshot_path}Capchadevnuxbet.png")
            break


general_run()
browser.close()
