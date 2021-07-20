from time import sleep
import random
import commonFunctions
import config

browser = commonFunctions.browser
screenshot_path = config.SCREENSHOT_PATH_AUTHORISATION
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
authorization_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"


def random_four_digits_number():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for iterable_element_in_sequence_of_numbers_created_by_range in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits


user_name = "autotestuser" + random_four_digits_number()


def authorisation_form_open():
    browser.find_element_by_css_selector(".regBtn").click()
    commonFunctions.wait_for_element(authorization_form_checkpoint)
    browser.refresh()
    commonFunctions.wait_for_element(authorization_form_checkpoint)
    try:
        browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
        sleep(1)
        browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
        print("login-registration swap, OK")
    except Exception as e:
        print(f"login-registration swap, NotOK, {e}")


def fill_one_field(element_xpath, element_data, element_name):
    try:
        browser.find_element_by_xpath(element_xpath).send_keys(element_data)
    except Exception as e:
        print(f"u{element_name} input Error, {e}")

def fill_fields():
    fill_one_field("//input[@type='text']", user_name, "username")
    fill_one_field("//input[@type='password']", config.PASSWORD, "password")
    fill_one_field("(//input[@type='password'])[2]", config.PASSWORD, "password confirmation")
    try:
        terms_checkbox = browser.find_element_by_xpath("//form/div/div/label")
        browser.execute_script("arguments[0].click();", terms_checkbox)
    except Exception as e:
        print(f"T&C Error, {e}")
    password_visibility()


def password_visibility():
    try:
        browser.find_element_by_css_selector(".passWrap:nth-child(4) > .showPass").click()
        browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[5]/div").click()
    except Exception as e:
        print(f"password vizibility Error, {e}")
    if browser.find_element_by_xpath("(//input[@type='text'])[2]").get_attribute("value") == config.PASSWORD:
        print("password vizibility, OK")
    else:
        print("password vizibility, NotOK")
    if browser.find_element_by_xpath("(//input[@type='text'])[3]").get_attribute("value") == config.PASSWORD:
        browser.save_screenshot(f"{screenshot_path}VisiblePasswordSFront1Nuxbet.png")
        print("password confirmation visibility, OK")
    else:
        print("password confirmation visibility, NotOK")


def log_out():
    commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    try:
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/span[1]").click()
        sleep(1)  # ждем появления дропдаyн меню
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/div[2]/a[7]").click()
        commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    except Exception as e:
        print(f"log out Error, {e}")
        browser.close()
    print("loged out")


commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
commonFunctions.register_open(authorization_form_checkpoint)
fill_fields()
browser.save_screenshot(f"{screenshot_path}SFront1Nuxbet.png")
print(f"Username: {user_name}\nPassword: {config.PASSWORD}")
sleep(2)
browser.find_element_by_xpath("//div[6]/button").click()
sleep(1)
if browser.page_source.find(user_name) > 0:
    print("registration, OK")
else:
    print("registration, NotOK")
log_out()
browser.close()
