from time import sleep
from datetime import date
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config
import logging

logging.basicConfig(filename="coefficientsNuxbet.log", level=logging.INFO, filemode="a",
                    format="%(name)s - %(levelname)s - %(asctime)s - %(message)s", datefmt='%d-%b-%y %H:%M:%S')
log_variable = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('coefficientsNuxbet.log')
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")

browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH, options=chrome_options)
browser.set_window_size(1808, 1020)
current_date = date.today()
screenshot_date = current_date.strftime("%d,%m,%Y")
screenshot_path = Path.cwd() / 'screenshots' / 'coef' / screenshot_date / 'a'
sports_list_id = {"Table Tennis": 13}
coef_list = []
main_coefs_list = []
logfile = open("coefficientsNuxbet.log", "a")


def open_page(i):
    # COEFPAGE - for dev; COEFLIVEPAGEPROD - for live events; COEFLIVEPAGE - for live dev-events
    browser.get(f"{config.COEFPAGEPROD}{i}")
    wait_for_element("/html/body/div/div[2]/div/section/div[2]/div[2]")
    open_list_of_events()


def open_page_live(i):
    # COEFPAGE - for dev; COEFLIVEPAGEPROD - for live events; COEFLIVEPAGE - for live dev-events
    browser.get(f"{config.COEFLIVEPAGEPROD}{i}")
    wait_for_element("/html/body/div/div[2]/div/section/div[2]/div[2]")
    open_list_of_events()


def open_list_of_events():
    try:
        browser.find_element_by_css_selector(".mainBtn:nth-child(1)").click()
        wait_for_element("/html/body/div/div[2]/div/section/div[2]/div[2]/div[1]")
        open_list_of_events()
    except:  # Тут ексепшн является условием выхода из рекурсии
        print("all opened")
        log_variable.info(f"all opened, Current URL: {browser.current_url}")


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 25).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"Element waiting error, Error, {e}")
        log_variable.error(f"Element waiting error, Error {e}")
        # browser.close()
        sleep(1)


def check_main_coefficients(sport_id):
    coefficient_mode = "Prematch"
    try:
        open_page(sport_id)
        elements = browser.find_elements_by_xpath("//div[@class='numbersWrap']")
        param_elements = (browser.find_elements_by_xpath("//div[@class='hasParams numbersWrap']"))
        max_number_of_digits = 2
        for coefficient_element in elements:
            coefficient_value = float(coefficient_element.text.split("\n")[-1])
            coef_list.append(coefficient_value)
            if len(str(coefficient_value)[-1].split(".")[-1]) > max_number_of_digits:
                print(f"too long coefficient, {coefficient_element}")
                log_variable.warning(f"too long coefficient, {coefficient_element}")
                # logfile.write(str(f"too long coefficient, {coefficient_element}"))
                browser.save_screenshot(f"{screenshot_path}DevNuxbet.png")
                coefficient_element.click()
                browser.save_screenshot(f"{screenshot_path}{coefficient_element.get_attribute('id')}Sport"
                                        f"{sport_id}Error.png")
        for param_coefficient_element in param_elements:
            # cutter_point = param_coefficient_element.get_attribute("innerText").find("\n") + 1
            coef_list.append(param_coefficient_element.text.split("\n")[-1])
        for coefficient_item in coef_list:
            if len(str(coefficient_item).split(".")[-1]) > max_number_of_digits:
                print(f"too long coeficient, {coefficient_item}")
            if float(coefficient_item) < 1.01 or float(coefficient_item) > 51:
                print(f"main coefficients Error, main coefficient value = {coefficient_item}, Sport id = {sport_id}")
                browser.save_screenshot(f"{screenshot_path}{coefficient_item}{sport_id}CoefErrorNuxbet.png")
        print(f"{coefficient_mode} Sport ID: {sport_id}, Main coefs: {coef_list}")
        log_variable.info(f"{coefficient_mode}Sport ID: {sport_id}, Main coefs: {coef_list}\n")
        # logfile.write(f"Sport ID: {sports_id}, Main coefs: {coef_list}\n")
        check_event_coefficients(coefficient_mode)
    except Exception as e:
        print(f"{sport_id} can't be reached, Error {e}")
        log_variable.warning(f"{sport_id} can't be reached, Error {e}")
        # logfile.write(f"{sports_id} can't be reached, Error {e}")


def check_main_coefficients_live(sport_id):
    coefficient_mode = "Live"
    try:
        open_page_live(sport_id)
        elements = browser.find_elements_by_xpath("//div[@class='numbersWrap']")
        param_elements = (browser.find_elements_by_xpath("//div[@class='hasParams numbersWrap']"))
        max_number_of_digits = 2
        for coefficient_element in elements:
            coefficient_value = float(coefficient_element.text.split("\n")[-1])
            coef_list.append(coefficient_value)
            if len(str(coefficient_value)[-1].split(".")[-1]) > max_number_of_digits:
                print(f"too long coefficient, {coefficient_element}")
                log_variable.warning(f"Live too long coefficient, {coefficient_element}")
                # logfile.write(str(f"too long coefficient, {coefficient_element}"))
                browser.save_screenshot(f"{screenshot_path}DevNuxbet.png")
                coefficient_element.click()
                browser.save_screenshot(f"{screenshot_path}{coefficient_element.get_attribute('id')}Sport"
                                        f"{sport_id}Error.png")
        for param_coefficient_element in param_elements:
            # cutter_point = param_coefficient_element.get_attribute("innerText").find("\n") + 1
            coef_list.append(param_coefficient_element.text.split("\n")[-1])
        for coefficient_item in coef_list:
            if len(str(coefficient_item).split(".")[-1]) > max_number_of_digits:
                print(f"too long coeficient, {coefficient_item}")
            if float(coefficient_item) < 1.01 or float(coefficient_item) > 51:
                print(f"main coefficients Error, main coefficient value = {coefficient_item}, Sport id = {sport_id}")
                browser.save_screenshot(f"{screenshot_path}{coefficient_item}{sport_id}CoefErrorNuxbet.png")
        print(f"{coefficient_mode} Sport ID: {sport_id}, Main coefs: {coef_list}")
        log_variable.info(f"{coefficient_mode} Sport ID: {sport_id}, Main coefs: {coef_list}\n")
        # logfile.write(f"Sport ID: {sports_id}, Main coefs: {coef_list}\n")
        check_event_coefficients(f"{coefficient_mode}")
    except Exception as e:
        print(f"{sport_id} can't be reached, Error {e}")
        log_variable.warning(f"{sport_id} can't be reached, Error {e}")
        # logfile.write(f"{sports_id} can't be reached, Error {e}")


def check_event_coefficients(mode):
    betmore_elements = browser.find_elements_by_xpath("//div[@class='leftSpace moreEvensWrap']/a")
    list_of_hrefs = []
    for betmore_element in betmore_elements:
        event_link = str(betmore_element.get_attribute("href"))
        list_of_hrefs.append(event_link)
    for event_link in list_of_hrefs:
        list_of_event_coefficients = []
        browser.get(event_link)
        wait_for_element("/html/body/div/div[2]/div/section[3]/div")
        sleep(1)
        event_coefficient_elements = browser.find_elements_by_xpath("//span[@class='odd']")
        for event_coefficient in event_coefficient_elements:
            list_of_event_coefficients.append(event_coefficient.text)
            try:
                if float(event_coefficient.text) < 1.01 or \
                        float(event_coefficient.text) > 51:
                    event_coefficient.click()
                    print(event_link)
                    browser.save_screenshot(f"{screenshot_path}{mode}{event_coefficient.text}EV{event_link[-7:]}DevNuxbet.png")
                    log_variable.warning(f"{mode} Event link:{str(event_link)}; Coefficient value: {event_coefficient.text}")
                    wait_for_element("//div[@class='betSlipInnerWrap']")
                    wait_for_element("//button[@id='resetBet']")
                    browser.find_element_by_xpath("//button[@id='resetBet']").click()
                    sleep(1)
            except Exception as e:
                print(f"Element check error, {e}")
                log_variable.error(f"{mode}Element check error, {e}")
                # logfile.write(f"Element check error, {e}")
        print(f" {mode} Event link: {event_link}; event-coefs:{list_of_event_coefficients}")
        log_variable.info(f" {mode} Event link: {event_link}; event-coefs:{list_of_event_coefficients}\n")


for sport in sports_list_id:
    check_main_coefficients(sports_list_id[sport])

for sport in sports_list_id:
    check_main_coefficients_live(sports_list_id[sport])
browser.close()
