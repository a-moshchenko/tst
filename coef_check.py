from time import sleep
from datetime import date
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--incognito")

browser = webdriver.Chrome(executable_path=Path.cwd() / "driwers" / "chromedriver.exe", options=chrome_options)
browser.set_window_size(1808, 1020)
current_date = date.today()
date = current_date.strftime("%d,%m,%Y")
screenshot_path = Path.cwd() / "screenshots" / "coef" / date
sports_list_id = {"Basketball": 2, "Tennis": 8, "AFL": 20, "Baseball": 1, "Beach Volleyball": 29,
                  "Boxing / UFC": 18, "Cricket": 24, "Darts": 12, "E-Sports": 21, "Futsal": 4, "Handball": 5,
                  "Hockey": 6, "Rugby": 15, "Snooker": 11, "Table Tennis": 13, "Volleyball": 9, "Soccer": 7}
coef_list = []
main_coefs_list = []
logfile = open("betsNuxbetLog.txt", "a")


def open_page(i):
    browser.get(f"https://dev.nuxbet.com/pre-match?sport_id={i}")
    wait_for_element("/html/body/div/div[2]/div/section/div[2]/div[2]")
    open_list_of_events()


def open_list_of_events():
    try:
        browser.find_element_by_css_selector(".mainBtn:nth-child(1)").click()
        wait_for_element("/html/body/div/div[2]/div/section/div[2]/div[2]/div[1]")
        open_list_of_events()
    except:  # Тут ексепшн является условием выхода из рекурсии
        print("all opened")


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 20).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"Element waiting error, Error, {e}")
        # browser.close()


def check_main_coeficients(sports_id):
    try:
        open_page(sports_id)
    except Exception as e:
        print(f"{sports_id} can't be reached, Error {e}")
    elements = browser.find_elements_by_xpath("//div[@class='numbersWrap']")
    param_elements = (browser.find_elements_by_xpath("//div[@class='hasParams numbersWrap']"))
    for coeficient_element in elements:
        coef_list.append(float(coeficient_element.get_attribute("innerText")[coeficient_element.get_attribute(
            "innerText").find("\n") + 1:]))
        if len(str(coeficient_element.get_attribute("innerText")[coeficient_element.get_attribute(
                "innerText").find("\n") + 1:]).split(".")[-1]) < 2:
            print(f"too long coeficient, {coeficient_element}")
            logfile.write(f"too long coeficient, {coeficient_element}")
            browser.save_screenshot(f"{screenshot_path}DevNuxbet.png")
            coeficient_element.click()
            browser.save_screenshot(f"{screenshot_path}{coeficient_element.get_attribute('id')}Sport"
                                    f"{sports_id}Error.png")
    for param_coeficient_element in param_elements:
        coef_list.append(param_coeficient_element
                         .get_attribute("innerText")[
                         param_coeficient_element.get_attribute("innerText").find("\n") + 1:])
    for i in coef_list:
        if len(str(i).split(".")[-1]) > 2:
            print(f"too long coeficient, {i}")
        if float(i) < 1.01 or float(1) > 51:
            print(f"main coeficients Error, main coeficient value = {i}, Sport id = {sports_id}")
            browser.save_screenshot(f"{screenshot_path}{i}{sports_id}CoefErrorNuxbet.png")
    print(f"Sport ID: {sports_id}, Main coefs: {coef_list}")
    logfile.write(f"Sport ID: {sports_id}, Main coefs: {coef_list}\n")
    ceck_subcoeficients()


def ceck_subcoeficients():
    betmore_elements = browser.find_elements_by_xpath("//div[@class='leftSpace moreEvensWrap']/a")
    list_of_hrefs = []
    for i in betmore_elements:
        event_link = str(i.get_attribute("href"))
        list_of_hrefs.append(str(event_link))
    for k in list_of_hrefs:
        list_of_subcoeficients = []
        browser.get(k)
        wait_for_element("/html/body/div/div[2]/div/section[3]/div")
        sleep(1)
        sub_coeficient_elements = browser.find_elements_by_xpath("//span[@class='odd']")
        for j in sub_coeficient_elements:
            list_of_subcoeficients.append(j.get_attribute("innerText"))
            try:
                if float(j.get_attribute("innerText")) < 1.01 or float(j.get_attribute("innerText")) > 51:
                    j.click()
                    browser.save_screenshot(str(f"{screenshot_path}{j.get_attribute('innerText')}{k}DevNuxbet.png"))
                    wait_for_element("//div[@class='betSlipInnerWrap']")
                    wait_for_element("//button[@id='resetBet']")
                    browser.find_element_by_xpath("//button[@id='resetBet']").click()
                    sleep(1)
            except Exception as e:
                print(f"Element check error, {e}")
        print(f" Event link: {k}; Sub-coefs:{list_of_subcoeficients}")
        logfile.write(f" Event link: {k}; Sub-coefs:{list_of_subcoeficients}\n")


for sport in sports_list_id:
    check_main_coeficients(sports_list_id[sport])
browser.close()
