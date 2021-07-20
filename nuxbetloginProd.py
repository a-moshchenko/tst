from time import sleep
import commonFunctions
import config

browser = commonFunctions.browser
screenshot_path = config.SCREENSHOT_PATH_AUTHORISATION
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
logout_dropdown_menu = "/html/body/div/div[2]/div/section[4]/header"


def password_visibility_check():
    # Проверяем отображение пароля при нажатии на глаз
    browser.find_element_by_css_selector(".showPass").click()
    sleep(1)
    password_vizible = str(browser.find_element_by_xpath("(//input[@type='text'])[2]").get_attribute("value"))
    try:
        if password_vizible == config.PASSWORD:
            browser.save_screenshot(f"{config.SCREENSHOT_PATH_AUTHORISATION}VisiblePasswordNuxbet.png")
            print("password vizible, OK")
        else:
            print("password vizible, NotOK")
    except Exception as e:
        print(f"password vizible, Error, {e}\n password: {password_vizible}")


def login_positive_flow():
    commonFunctions.open_page(config.SITE_PROD, main_page_checkpoint)
    browser.find_element_by_css_selector(".loginBtn").click()

    try:
        browser.find_element_by_css_selector(".formHeader")
        print("auth form, OK")
    except Exception as e:
        print(f"auth form, NotOK, {e}")
    login_mail = browser.find_element_by_xpath("//input[@type='text']")
    login_mail.send_keys(config.AUTHORISATION_NAME_EXIST)
    password = browser.find_element_by_xpath("//input[@type='password']")
    password.send_keys(config.PASSWORD)
    sleep(1)  # слип нужен, чтоб изменения отобразились в браузере
    password_visibility_check()
    login_button = browser.find_element_by_css_selector(".btnWrap > .mainBtn")
    login_button.click()
    sleep(2)
    try:
        uname = browser.find_element_by_xpath("//span[@class='userName ellipsis']")
        if uname.text == config.AUTHORISATION_NAME_EXIST:
            browser.save_screenshot(f"{config.SCREENSHOT_PATH_AUTHORISATION}LogedInNuxbet.png")
            print("auth, OK\nmain page return, OK")
        else:
            print("NOK, uname: ", uname.text)
    except Exception as e:
        print(f"auth, NotOK, {e}")
    log_out()


def log_out():
    commonFunctions.wait_for_element(logout_dropdown_menu)
    print("page loaded")
    try:
        browser.find_element_by_xpath("//span[@class='userName ellipsis']").click()
        sleep(1)
        browser.find_element_by_xpath("//a[@href='#']").click()
    except Exception as e:
        print(f"logged out, {e}")


def login_negative_flow():
    commonFunctions.open_page(config.SITE_PROD, main_page_checkpoint)
    try:
        log_out()
    except Exception as e:
        print(f"Loged out, {e}")
    browser.find_element_by_css_selector(".loginBtn").click()
    try:
        browser.find_element_by_css_selector(".formHeader")
        print("auth form, OK")
    except Exception as e:
        print(f"auth form, NotOK, {e}")
    login_mail = browser.find_element_by_xpath(
        "//input[@type='text']")  # проверка почты без собаки и незаполненный пароль
    login_mail.send_keys("noatmail")
    login_button = browser.find_element_by_xpath("//button[@class='mainBtn']")
    login_button.click()
    sleep(1)  # слип нужен чтоб форма обновилась
    if login_mail.get_attribute("class") == "inputError":
        print("mail !@, OK")
    else:
        print("mail !@, NotOK")
    if browser.find_element_by_xpath("//input[@type='password']").get_attribute("class") == "inputError":
        print("no password, OK")
    else:
        print("no password, NotOK")
    if browser.page_source.find("Enter valid email address") > 0:
        print("mail error messaage, OK")
    else:
        print("mail error messaage, OK")
    if browser.page_source.find("This field is required") > 0:
        browser.save_screenshot(f"{config.SCREENSHOT_PATH_AUTHORISATION}NoEtMailNoPasswordNuxbet.png")
        print("empty field message, OK")
    else:
        print("empty field message, OK")

    login_mail = browser.find_element_by_xpath(
        "//input[@type='text']")  # проверка валидной почты с незаполненным паролем
    login_mail.send_keys(config.AUTHORISATION_NAME_EXIST)
    login_button = browser.find_element_by_css_selector(".btnWrap > .mainBtn")
    login_button.click()
    sleep(1)  # слип нужен чтоб форма обновилась
    if login_mail.get_attribute("class") != "inputError":
        browser.save_screenshot(f"{config.SCREENSHOT_PATH_AUTHORISATION}NoPasswordNuxbet.png")
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
        browser.save_screenshot(f"{config.SCREENSHOT_PATH_AUTHORISATION}WrongPasswordNuxbet.png")
        print("invalid password message, OK")
    else:
        print("invalid password message, NotOK")
    browser.refresh()


login_positive_flow()
browser.refresh()
login_negative_flow()
browser.close()
