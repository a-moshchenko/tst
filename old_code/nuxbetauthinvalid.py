from time import sleep
from selenium.webdriver.common.keys import Keys
import commonFunctions
import config

browser = commonFunctions.browser
screenshot_path = config.SCREENSHOT_PATH_AUTHORISATION
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
registration_form_checkpoint = "/html/body/div/div[2]/div/section/div"


def warning_check(element_xpath, element_name):
    if browser.find_element_by_xpath(element_xpath).get_attribute("class") == "inputError":
        print(f"requiring {element_name} alert, OK")
    else:
        print(f"requiring {element_name} alert, NotOK")


def password_confirmation_error():
    commonFunctions.open_page(config.SITE, main_page_checkpoint)
    commonFunctions.register_open(registration_form_checkpoint)
    # Вводим пароль и некорректное подтверждение
    password_field = browser.find_element_by_xpath("//input[@type='password']")
    password_field.click()
    password_field.send_keys(config.PASSWORD)
    sleep(1)  # слип нужен для разделения ввода
    password_field.send_keys(Keys.TAB)

    password_confirm_field = browser.find_element_by_xpath("(//input[@type='password'])[2]")
    password_confirm_field.click()
    password_confirm_field.send_keys("secretZ2")
    password_confirm_color = password_confirm_field.get_attribute("class")
    if password_confirm_color == "inputError":
        browser.save_screenshot(f"{screenshot_path}PasswordConfirmationDevNuxbet.png")
        print("confirmation, OK")
    else:
        print("confirmation, NotOK")


def invalid_email_error():
    # Вводим емайл без собаки
    commonFunctions.open_page(config.SITE, main_page_checkpoint)
    email_field = browser.find_element_by_xpath("//form/div/div/input")
    email_field.click()
    email_field.send_keys("qwertry")
    registration_button = browser.find_element_by_xpath(
        "//button[@class='mainBtn']")
    registration_button.click()
    if not commonFunctions.capcha_finder():
        return None
    warning_check("//input[@type='text']", "main button")
    if browser.page_source.find("Enter valid email address") > 0:
        print("e-mail errMsg, OK")
    else:
        print("e-mail errMsg, NotOK")

    # Вводим емайл без домена
    commonFunctions.open_page(config.SITE, main_page_checkpoint)
    sleep(1)
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.click()
    email_field.send_keys("qwertry@")
    registration_button = browser.find_element_by_xpath(
        "//button[@class='mainBtn']")
    registration_button.click()
    if not commonFunctions.capcha_finder():
        return None
    if email_field.get_attribute("class") == "inputError":
        browser.save_screenshot(f"{screenshot_path}NoDomainMailDevNuxbet.png")
        print("no domain mail, OK")
    else:
        print("no domain mail, NotOK")

    # Вводим мейл с кириллицей
    commonFunctions.open_page(config.SITE, main_page_checkpoint)
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.click()
    email_field.send_keys("почта@домен.сру")
    browser.find_element_by_xpath("//input[2]").send_keys(config.AUTHORISATION_NAME)  # вводим имя пользователя
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(config.PASSWORD)  # подтверждаем пароль
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/label")))  # соглашаемся с T&C
    registration_button = browser.find_element_by_xpath(
        "//button[@class='mainBtn']")
    registration_button.click()
    if not commonFunctions.capcha_finder():
        return None
    sleep(1)  # слип нужен чтоб дать форме измениться
    if browser.page_source.find("Wrong") > 0:
        browser.save_screenshot(f"{screenshot_path}CyrilykMailDevNuxbet.png")
        print("cyrylik mail, OK")
    else:
        print("cyr mail, NotOK")

    # Вводим мейл с пробелом
    commonFunctions.open_page(config.SITE, main_page_checkpoint)
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.send_keys('"space mail"@mail.u')
    registration_button = browser.find_element_by_xpath(
        "//button[@class='mainBtn']")
    registration_button.click()
    if not commonFunctions.capcha_finder():
        return None
    if email_field.get_attribute("class") == "inputError":
        print("space domain, OK")
    else:
        print("space domain, NotOK")

    # Вводим ранее зарегистрированный мейл
    browser.refresh()
    email_field = browser.find_element_by_xpath("//input[@type='text']")
    email_field.click()
    email_field.send_keys(config.AUTHORISATION_NAME)
    browser.find_element_by_xpath(
        "(//input[@type='text'])[2]").send_keys(config.AUTHORISATION_NAME)  # вводим имя пользователя
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(config.PASSWORD)  # подтверждаем пароль
    browser.execute_script("arguments[0].click();", (browser.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/label")))  # соглашаемся с T&C
    registration_button = browser.find_element_by_xpath(
        "//button[@class='mainBtn']")
    registration_button.click()
    if not commonFunctions.capcha_finder():
        return None
    if browser.page_source.find("Username/Email already exist") > 0:
        browser.save_screenshot(f"{screenshot_path}UsedMailDevNuxbet.png")
        print("used mail alert, OK")
    else:
        print("used mail alert, OK")


def reqested_fields_empty():
    # Проверка алертов на незаполненых обязательных полях
    browser.refresh()
    browser.find_element_by_xpath(
        "//button[@class='mainBtn']").click()  # нажимаем "зарегистрироваться" в форме регистрации
    sleep(1)  # нужен чтоб форма успела обновиться
    if not commonFunctions.capcha_finder():
        return None
    warning_check("//input[@type='text']", "mail")
    warning_check("(//input[@type='text'])[2]", "name")  # проверяем наличие ворнинга в поле имени пользователя
    warning_check("//input[@type='password']", "password")  # проверяем наличие ворнинга в поле пароля
    warning_check("(//input[@type='password'])[2]",
                  "password confirmation")  # проверяем наличие ворнинга в поле подтверждения пароля
    warning_check("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/label", "T&C")
    browser.save_screenshot(f"{screenshot_path}EmptyFieldsDevNuxbet.png")


def login_through_auth():
    # проверка перехода на форму логина с формы регистрации
    browser.refresh()
    browser.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
    sleep(1)  # ждем пока форма сменится
    if browser.current_url == f"{config.SITE}":
        print("goto login, OK")
    else:
        print("goto login, NotOK")


password_confirmation_error()
invalid_email_error()
reqested_fields_empty()
login_through_auth()
browser.close()
