from time import sleep
from selenium.common.exceptions import NoSuchElementException
import commonFunctions
import config

browser = commonFunctions.browser
screenshot_path = config.SCREENSHOT_PATH_AUTHORISATION
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
logout_form_checkpoint = "/html/body/div/div[2]/div/section[4]/header"


def password_visibility_check():
    # Проверяем отображение пароля при нажатии на глаз
    browser.find_element_by_xpath("//div[3]/div").click()
    sleep(1)
    password_visible = str(browser.find_element_by_xpath("//div[3]/input").get_attribute("value"))
    try:
        if password_visible == config.PASSWORD:
            browser.save_screenshot(f"{screenshot_path}VisiblrPasswordDevNuxbet.png")
            print("password visible, OK")
        else:
            print("password visible, NotOK")
    except Exception as e:
        print(f"password visible, Error, {e}\n{password_visible}")


def login_positive_flow():
    commonFunctions.open_page(config.SITE, main_page_checkpoint)
    browser.find_element_by_xpath("//div[3]/a").click()
    try:
        browser.find_element_by_css_selector(".formHeader")
        print("auth form, OK")
    except Exception as e:
        print(f"auth form, NotOK, Error {e}")
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHORISATION_NAME_EXIST)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    sleep(1)  # слип нужен, чтоб изменения отобразились в браузере
    password_visibility_check()
    browser.find_element_by_xpath("//form/div[2]/button").click()
    sleep(2)
    try:
        user_name = browser.find_element_by_xpath("//div[2]/div[3]")
        if user_name.text == config.AUTHORISATION_NAME_EXIST:
            print("authorisation, OK\n main page return, OK")
            browser.save_screenshot(f"{screenshot_path}UserLogedInDevNuxbet.png")
        else:
            print(f"NOK, uname: {user_name.text}")
    except Exception as e:
        print(f"authorisation, NotOK, {e}")
    log_out()


def log_out():
    commonFunctions.wait_for_element(logout_form_checkpoint)
    print("page loaded")
    try:
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/span[2]").click()
        commonFunctions.wait_for_element("/html/body/div/div[1]/div/div/div[2]/div[3]/div[2]/a[8]")
        sleep(1)
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/div[2]/a[8]").click()
    except NoSuchElementException:  # ексепшн является частью позитив флоу
        print("logged out")


def login_negative_flow():
    commonFunctions.open_page(config.SITE, main_page_checkpoint)
    commonFunctions.wait_for_element("//div[3]/a")
    browser.find_element_by_xpath("//div[3]/a").click()
    try:
        browser.find_element_by_css_selector(".formHeader")
        print("authorisation form, OK")
    except Exception as e:
        print(f"authorisation form, NotOK, {e}")
    commonFunctions.wait_for_element("//input[@type='text']")
    login_mail = browser.find_element_by_xpath("//input[@type='text']")  # проверка почты без собаки и без пароля
    browser.find_element_by_xpath("//input[@type='text']").send_keys("noatmail")
    login_button = browser.find_element_by_xpath("//form/div[2]/button")
    login_button.click()
    sleep(1)  # слип нужен чтоб форма обновилась
    if login_mail.get_attribute("class") == "inputError":
        browser.save_screenshot(f"{screenshot_path}NoEtMailLoginDevNuxbet.png")
        print("mail without et, OK")
    else:
        print("mail without et, NotOK")
    if browser.find_element_by_xpath("//div[1]/div[4]/input").get_attribute("class") == "inputError":
        print("no password, OK")
    else:
        print("no password, NotOK")
    if browser.page_source.find("Enter valid email address") > 0:
        print("mail error message, OK")
    else:
        print("mail error message, NotOK")
    if browser.page_source.find("This field is required") > 0:
        print("empty field message, OK")
    else:
        print("empty field message, NotOK")

    login_mail = browser.find_element_by_xpath("//input[@type='text']")  # проверка почты с незаполненным паролем
    login_mail.send_keys(config.AUTHORISATION_NAME_EXIST)
    login_button = browser.find_element_by_xpath("//form/div[2]/button")
    login_button.click()
    sleep(1)  # слип нужен чтоб форма обновилась
    if login_mail.get_attribute("class") != "inputError":
        browser.save_screenshot(f"{screenshot_path}NoMailDevNuxbet.png")
        print("valid mail, OK")
    else:
        print("valid mail, NotOK")
    browser.refresh()

    login_mail = browser.find_element_by_xpath("//input[@type='text']")  # проверка валидной почты с неверным паролем
    login_mail.send_keys(config.AUTHORISATION_NAME_EXIST)
    login_button = browser.find_element_by_xpath("//form/div[2]/button")
    password = browser.find_element_by_xpath("//input[@type='password']")
    password.send_keys("password")
    login_button.click()
    sleep(1)  # слип нужен чтоб форма обновилась
    if browser.page_source.find("Incorrect login or password. Please check again."):
        browser.save_screenshot(f"{screenshot_path}WrongPasswordLoginPasswordDevNuxbet.png")
        print("invalid password message, OK")
    else:
        print("invalid password message, NotOK")
    browser.refresh()


login_positive_flow()
browser.refresh()
login_negative_flow()
browser.close()
