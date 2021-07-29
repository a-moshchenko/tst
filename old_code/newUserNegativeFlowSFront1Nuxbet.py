from time import sleep
import random
import commonFunctions
import config

browser = commonFunctions.browser
screenshot_path = config.SCREENSHOT_PATH_AUTHORISATION
authorisation_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"


def random_four_digits_number():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for iterable_element_in_sequence_of_numbers_created_by_range in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits


user_name = f"autotestuser{random_four_digits_number()}"


def authorisation_form_open():
    sleep(1)
    browser.find_element_by_css_selector(".regBtn").click()
    commonFunctions.wait_for_element(authorisation_form_checkpoint)
    browser.refresh()
    commonFunctions.wait_for_element(authorisation_form_checkpoint)


def warning_check(object_address, checked_object):
    if browser.find_element_by_xpath(object_address).get_attribute("class") == "inputError":
        print(f"no {checked_object} warning, OK")
    else:
        print(f"no {checked_object} warning, NotOK")


def negative_flow_authorization():
    # проверяем пустые поля
    authorisation_form_open()
    browser.find_element_by_xpath("//div[6]/button").click()
    if not commonFunctions.capcha_finder():
        return None
    warning_check("//input[@type='text']", "username")
    warning_check("//input[@type='password']", "password")
    warning_check("(//input[@type='password'])[2]", "password confirmation")
    warning_check("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/label", "T&C confirmation")
    browser.save_screenshot(f"{screenshot_path}EmptyFieldsSFront1Nuxbet.png")

    # проверяем без паролей
    commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    browser.find_element_by_xpath("//input[@type='text']").send_keys("autotestuser0000")
    browser.find_element_by_xpath("//div[6]/button").click()
    if not commonFunctions.capcha_finder():
        return None
    if browser.find_element_by_xpath("//input[@type='text']").get_attribute("class") != "inputError":
        print("no username warning, OK")
    else:
        print("no username warning, NotOK")
    warning_check("//input[@type='password']", "password")
    warning_check("(//input[@type='password'])[2]", "password confirmation")
    warning_check("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/label", "T&C confirmation")
    if browser.page_source.find("shortText.field_required") > 0 or browser.page_source.find(
            "This field is required") > 0:
        print("required field message, OK")
    else:
        print("required field message, NotOK")
    browser.save_screenshot(f"{screenshot_path}EmptyPasswordsSFront1Nuxbet.png")

    # проверяем с неправильным подтверждением пароля
    commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    # auth_open()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("autotestuser0000")
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("secretZ2")
    browser.find_element_by_css_selector(".passWrap:nth-child(4) > .showPass").click()
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[5]/div").click()
    warning_check("(//input[@type='text'])[3]", "password confirmation")
    browser.save_screenshot(f"{screenshot_path}WrongPasswordConfirmationSFront1Nuxbet.png")

    # проверяем с нечекнутым T&C боксом
    commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    browser.find_element_by_xpath("//input[@type='text']").send_keys("autotestuser0000")
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("//div[6]/button").click()
    if not commonFunctions.capcha_finder():
        return None
    warning_check("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/label", "T&C confirmation")

    # проверяем киррилицу в поле юзернейм
    commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    # auth_open()
    browser.find_element_by_xpath("//input[@type='text']").send_keys("юзернейм")
    warning_check("//input[@type='text']", "cyrylik username")
    browser.save_screenshot(f"{screenshot_path}CyrylikUsernameSFront1Nuxbet.png")

    # проверяем ранее зарегистрированный юзернейм
    commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(config.AUTHORISATION_SHORT_NAME)
    browser.find_element_by_xpath("//input[@type='password']").send_keys("secretZ2")
    browser.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("secretZ2")
    try:
        terms_checkbox = browser.find_element_by_xpath("//form/div/div/label")
        browser.execute_script("arguments[0].click();", terms_checkbox)
    except Exception as e:
        print(f"T&C Error, {e}")
    browser.find_element_by_xpath("//div[6]/button").click()
    sleep(1)  # нужно чтоб форма обновилась
    if not commonFunctions.capcha_finder():
        return None
    if browser.page_source.find("Username/Email already exist") > 0:
        print("ExistingUser warning, OK")
    else:
        print("ExistingUser warning, NotOK")
    browser.save_screenshot(f"{screenshot_path}ExistingUsernameSFront1Nuxbet.png")


commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
negative_flow_authorization()
browser.close()
