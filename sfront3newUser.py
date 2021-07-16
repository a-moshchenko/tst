import random
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH, options=chrome_options)
current_date = date.today()
date = current_date.strftime("%d,%m,%Y")
screenshot_path = config.SCREENSHOTPATHAUTH
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
registration_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"
user_registration_info = {}


def random_four_digits_number():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for i in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"wait for element, Error, {e}, {xpath}")
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
        print(f"swich to login form1, NotOK, Error, {e}")
    try:
        wait_for_element("//div[@class='formWrap authForm fullForm']")
        print("swich to registration form, OK")
    except Exception as e:
        print(f"swich to registration form, NotOK, Error, {e}")


def empty_fields_check():
    browser.find_element_by_xpath("//div[7]/button").click()
    sleep(1)  # нужно чтоб форма обновилась
    if browser.find_element_by_xpath("(//input[@type='text'])[4]").get_attribute("class") == "inputError":
        print("empty email field warning, OK")
    else:
        print("empty email field warning, NotOK")
    try:
        browser.find_element_by_xpath(
            "//div[@class='v-select customSelect secondColor vs--single vs--searchable inputError']")
        print("empty currency field warning, OK")
    except Exception as e:
        print(f"empty currency field warning, NotOK, Error, {e}")
    if browser.find_element_by_xpath("//input[@type='password']").get_attribute("class") == "inputError":
        print("empty password field warning, OK")
    else:
        print("empty password field warning, NotOK")
    if browser.find_element_by_xpath("(//input[@type='password'])[2]").get_attribute("class") == "inputError":
        print("empty password confirmation field warning, OK")
    else:
        print("empty password confirmation field warning, NotOK")
    if browser.find_element_by_xpath("//div[2]/label").get_attribute("class") == "inputError":
        print("no T&C confirmation field warning, OK")
    else:
        print("no T&C confirmation field warning, NotOK")
    if str(browser.page_source).count("This field is required") == 5:
        print("empty fields warning messages, OK")
    else:
        print("empty fields warning messages, OK")
    browser.save_screenshot(f"{screenshot_path}EmptyFieldsWarningsSFront3Nuxbet.png")


def fill_all_fields():
    username = f"autotestuser{random_four_digits_number()}"
    browser.find_element_by_xpath("(//input[@type='text'])").send_keys(username)
    browser.find_element_by_xpath("(//input[@type='text'])[2]").send_keys("userSecondName")
    birth_date = browser.find_element_by_xpath("//input[@name='date']")
    birth_date.click()
    wait_for_element("//div[@class='mx-calendar-content']")
    move_calendar_right = browser.find_element_by_xpath("//button[@class='mx-btn mx-btn-text mx-btn-icon-right']")
    move_calendar_left = browser.find_element_by_xpath("//button[@class='mx-btn mx-btn-text mx-btn-icon-left']")
    move_calendar_right.click()
    browser.find_element_by_xpath("//tr[3]/td[4]/div").click()
    try:
        browser.find_element_by_xpath("//div[@class='mx-calendar-content']")
    except Exception:  # тут ексепшн используется как проверка наличия элемента
        print("too young user regisntation, NotOK")
    move_calendar_left.click()
    move_calendar_left.click()
    browser.find_element_by_xpath("//tr[3]/td[3]").click()
    browser.find_element_by_xpath("(//input[@type='text'])[4]").send_keys(f"{username}@mail.com")
    browser.find_element_by_xpath("(//input[@type='search'])[5]").click()
    wait_for_element("//ul[@id='vs5__listbox']")
    browser.find_element_by_xpath("//li[@id='vs5__option-6']").click()
    browser.find_element_by_xpath("(//input[@type='text'])[5]").send_keys("Buchenvald")
    browser.find_element_by_xpath("(//input[@type='text'])[6]").send_keys("Palace")
    browser.find_element_by_xpath("(//input[@type='search'])[6]").send_keys("13")
    browser.find_element_by_xpath("(//input[@type='search'])[6]").send_keys(Keys.ENTER)
    browser.find_element_by_xpath("//input[@type='tel']").send_keys(f"321{random_four_digits_number()}")
    browser.find_element_by_xpath("//*[@id='vs7__combobox']/div[1]/input").click()
    browser.find_element_by_xpath("(//input[@type='search'])[7]").send_keys("GBP")
    browser.find_element_by_xpath("(//input[@type='search'])[7]").send_keys(Keys.ENTER)
    sleep(1)
    browser.find_element_by_xpath("//*[@id='vs7__combobox']").click()
    wait_for_element("//*[@id='vs7__option-3']")
    browser.find_element_by_xpath("//*[@id='vs7__option-6']").click()
    browser.find_element_by_xpath("(//input[@type='text'])[7]").send_keys(f"{username}Login")
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("//div[2]/div[3]/div").click()
    if str(browser.find_element_by_xpath("(//input[@type='text'])[8]").get_attribute("value")) == config.PASSWORD:
        print("password visibility, OK")
    else:
        print("password visibility, NotOK")
    sleep(1)
    browser.find_element_by_xpath("//input[@type='password']") \
        .send_keys(config.PASSWORD)
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div[2]/div[5]/div").click()
    if str(browser.find_element_by_xpath("(//input[@type='text'])[9]").get_attribute("value")) == config.PASSWORD:
        print("password confirmation visibility, OK")
    else:
        print("password confirmation visibility, NotOK")
    browser.find_element_by_xpath("(//input[@type='text'])[10]") \
        .send_keys(config.REFCODE)
    terms_checkbox = browser.find_element_by_xpath("//div[2]/label")
    browser.execute_script("arguments[0].click();", terms_checkbox)
    browser.save_screenshot(f"{screenshot_path}RegistrationFormFilledSFront3Nuxbet.png")


def invalid_email_check():
    # Проверяем регистрацию уже зарегистрированного пользователя
    fill_all_fields()
    browser.find_element_by_xpath("(//input[@type='text'])[4]").send_keys(Keys.CONTROL + "a")
    browser.find_element_by_xpath("(//input[@type='text'])[4]").send_keys(Keys.DELETE)
    browser.find_element_by_xpath("(//input[@type='text'])[4]").send_keys(config.AUTHNAME)
    browser.find_element_by_css_selector(".btnWrap > .mainBtn").click()
    sleep(1)  # нужно чтоб форма обновилась
    if str(browser.page_source).find("Username/Email already exist") > 0:
        print("exsisting user registration, OK")
    else:
        print("exsisting user registration, NotOK")
    browser.save_screenshot(f"{screenshot_path}ExsistingUserRegistrationSFront3Nuxbet.png")
    browser.refresh()

    # Проверяем почту с кирилицей
    fill_all_fields()
    browser.find_element_by_xpath("(//input[@type='text'])[4]").send_keys(Keys.CONTROL + "a")
    browser.find_element_by_xpath("(//input[@type='text'])[4]").send_keys(Keys.DELETE)
    browser.find_element_by_xpath("(//input[@type='text'])[4]").send_keys("почта@домен.сру")
    browser.find_element_by_css_selector(".btnWrap > .mainBtn").click()
    if str(browser.page_source).find("Enter valid email address") > 0:
        print("cyrylic email warning, OK")
    else:
        print("cyrylic email warning, NotOK")
    browser.save_screenshot(f"{screenshot_path}CyrylicEmailSFront3Nuxbet.png")
    browser.refresh()

    # Проверяем почту без домена и собаки
    fill_all_fields()
    browser.find_element_by_xpath("(//input[@type='text'])[4]").send_keys(Keys.CONTROL + "a")
    browser.find_element_by_xpath("(//input[@type='text'])[4]").send_keys(Keys.DELETE)
    browser.find_element_by_xpath("(//input[@type='text'])[4]").send_keys(config.AUTHSHORTNAME)
    browser.find_element_by_css_selector(".btnWrap > .mainBtn").click()
    if str(browser.page_source).find("Enter valid email address") > 0:
        print("no et email warning, OK")
    else:
        print("no et email warning, NotOK")
    browser.save_screenshot(f"{screenshot_path}NoEtEmailSFront3Nuxbet.png")
    browser.refresh()

    # проверяем неверное подтверждение пароля
    fill_all_fields()
    browser.find_element_by_xpath("(//input[@type='text'])[8]").send_keys(Keys.BACKSPACE)
    browser.save_screenshot(f"{screenshot_path}IncorrectPasswordConfirmationSFront3Nuxbet.png")
    if str(browser.find_element_by_xpath("(//input[@type='text'])[9]").get_attribute("class")) == "inputError":
        print("wrong password confirmation field warning, OK")
    else:
        print("wrong password confirmation field warning, NotOK")
    browser.save_screenshot(f"{screenshot_path}PasswordConfirmationWarningSFront3Nuxbet.png")
    browser.refresh()


def registration_negative_flow():
    try:
        browser.find_element_by_xpath("//div[@class='btnWrap regBtn']")
    except Exception:  # тут ексепшн использован для проверки наличия открытой формы регистрации, поэтому он не описан
        open_registration_form()
    empty_fields_check()
    browser.refresh()
    invalid_email_check()


def log_out():
    browser.find_element_by_css_selector(".userName").click()
    wait_for_element("//a[contains(@href, '#')]")
    sleep(1)
    browser.find_element_by_xpath("//a[contains(@href, '#')]").click()
    browser.refresh()
    wait_for_element("/html/body/div/div[2]/div/section[2]/div")


def login_via_google():
    open_registration_form()
    browser.find_element_by_xpath("//img[@alt='google']").click()
    wait_for_element("//input[@id='identifierId']")
    browser.find_element_by_xpath(
        "//input[@id='identifierId']").send_keys(config.DEFAULTMAIL)
    browser.find_element_by_xpath("//input[@id='identifierId']").send_keys(Keys.ENTER)
    sleep(1)
    wait_for_element("//*[@id='password']/div[1]/div/div[1]/input")
    browser.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input").send_keys(config.PASSWORD)
    sleep(1)
    browser.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input").send_keys(Keys.ENTER)
    wait_for_element(main_page_checkpoint)
    sleep(3)
    browser.save_screenshot(f"{screenshot_path}RegistratedViaGoogleSFront3Nuxbet.png")
    if str(browser.page_source).find("nuxbetchk") > 0:
        print("google login, OK")
    else:
        print("google login, NotOK")


def registration_positive_flow():
    fill_all_fields()
    username = str(browser.find_element_by_xpath("(//input[@type='text'])[4]").get_attribute("value"))[:-9]
    print(f"""Username: {username}\nPassword: {config.PASSWORD}\nPhone: {browser.find_element_by_xpath(
        "//input[@type='tel']").get_attribute("value")}""")
    global user_registration_info
    user_registration_data(user_registration_info)
    browser.find_element_by_xpath("//button[@class='mainBtn']").click()
    wait_for_element("/html/body/div/div[2]/div/section[2]/div")
    sleep(2)
    if str(browser.current_url) == str(config.SFRONT3SITE):
        print("to main page after registration, OK")
    else:
        print("to main page after registration, NotOK")
    if str(browser.page_source).find(username) > 0:
        print("user registered, OK")
    else:
        print("user registered, NotOK")
    browser.save_screenshot(f"{screenshot_path}RegistrationFinishedSFront3Nuxbet.png")
    log_out()
    login_via_google()


def user_registration_data(user_data):
    user_data.update({"name": str(browser.find_element_by_xpath("(//input[@type='text'])").get_attribute("value"))})
    user_data.update({"second_name": str(browser.find_element_by_xpath("(//input[@type='text'])[2]").get_attribute(
        "value"))})
    user_data.update({"birthdate": str(browser.find_element_by_xpath("//input[@name='date']").get_attribute(
        "value"))})
    user_data.update({"email": str(browser.find_element_by_xpath("(//input[@type='text'])[4]").get_attribute("value"))})
    user_data.update({"country": str(browser.find_element_by_xpath("//*[@id='vs5__combobox']/div[1]/span"
                                                                   ).get_attribute("innerText"))})
    user_data.update({"city": str(browser.find_element_by_xpath("(//input[@type='text'])[5]").get_attribute("value"))})
    user_data.update({"adress": str(browser.find_element_by_xpath("(//input[@type='text'])[6]").get_attribute(
        "value"))})
    user_data.update({"mobile": str(browser.find_element_by_xpath("//*[@id='vs6__combobox']/div[1]/span").get_attribute(
        "innerText") + "-" + str(browser.find_element_by_xpath("//input[@type='tel']").get_attribute("value")))})
    user_data.update({"currency": str(browser.find_element_by_xpath("//*[@id='vs7__combobox']/div[1]/span"
                                                                    ).get_attribute("innerText"))})
    user_data.update({"username": str(browser.find_element_by_xpath("(//input[@type='text'])[7]").get_attribute(
        "value"))})
    user_data.update({"refer_code": str(browser.find_element_by_xpath("(//input[@type='text'])[10]").get_attribute(
        "value"))})
    return user_data


def admin_userdata_check():
    browser.get("https://sback.nuxbet.com/")
    browser.set_window_size(1100, 1020)
    sleep(2)
    browser.find_element_by_xpath("/html/body/div/div/div/form/div[1]/input").send_keys("sf3alexproc1313@gmail.com")
    browser.find_element_by_xpath("/html/body/div/div/div/form/div[1]/div[3]/input").send_keys("enemy1307")
    browser.find_element_by_xpath("/html/body/div/div/div/form/div[2]/button").click()
    wait_for_element("/html/body/div/header/a")
    browser.find_element_by_xpath("//a[contains(.,' Users')]").click()
    sleep(1)
    browser.find_element_by_xpath("//span[contains(.,'Players')]").click()
    browser.find_element_by_xpath("//*[@id='adminUsers_filter']/label/input").send_keys(user_registration_info["name"])
    browser.find_element_by_xpath("//*[@id='adminUsers_filter']/label/input").send_keys(Keys.ENTER)
    sleep(1)
    browser.find_element_by_css_selector("svg").click()
    browser.find_element_by_css_selector("div:nth-child(1) > ul > li:nth-child(1) > a").click()
    if str(browser.find_element_by_xpath("//input[@id='InputEmail']").get_attribute("value")) == \
            str(user_registration_info["email"]):
        print("email to DB, OK")
    else:
        print("email to DB, NotOK")
    if str(browser.find_element_by_xpath("//input[@id='InputUserName']").get_attribute("value")) == str(
            user_registration_info["username"]):
        print("username to DB, OK")
    else:
        print("username to DB, NotOK")
    if str(browser.find_element_by_xpath("//input[@id='InputPhone']").get_attribute("value")) == str(
            user_registration_info["mobile"]):
        print("phone to DB, OK")
    else:
        print("phone to DB, NotOK")
    if str(browser.find_element_by_xpath("//select[@id='currency']").get_attribute("value")) == str(
            user_registration_info["currency"]):
        print("currency to DB, OK")
    else:
        print("currency to DB, NotOK")
    if str(browser.find_element_by_xpath("//input[@name='country_id']").get_attribute("value")) == str(
            user_registration_info["country"]):
        print("country to DB, OK")
    else:
        print("country to DB, NotOK")
    if str(browser.find_element_by_xpath("//input[@name='city']").get_attribute("value")) == str(
            user_registration_info["city"]):
        print("city to DB, OK")
    else:
        print("city to DB, NotOK")
    if str(browser.find_element_by_xpath("//input[@name='street']").get_attribute("value")) == str(
            user_registration_info["adress"]):
        print("adress to DB, OK")
    else:
        print("adress to DB, NotOK")
    if str(browser.find_element_by_xpath("//input[@name='ref_code']").get_attribute("value")) == str(
            user_registration_info["refer_code"]):
        print("ref code to DB, OK")
    else:
        print("ref code to DB, NotOK")


open_main_page()
open_registration_form()
to_login_form_and_back()
registration_negative_flow()
registration_positive_flow()
admin_userdata_check()
browser.close()
