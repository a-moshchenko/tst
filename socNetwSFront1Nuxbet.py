from time import sleep
import random
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import commonFunctions
import config

# Перед запуском, по возможности, отключить капчу
print("Перед запуском, по возможности, отключить капчу")

browser = commonFunctions.browser
screenshot_path = config.SCREENSHOT_PATH_AUTHORISATION
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
authorisation_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"


def random_four_digits_number():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for iterable_element_of_sequence_of_numbers_created_by_range in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits


user_name = f"autotestuser{random_four_digits_number()}"


def authorisation_form_open():
    sleep(3)
    browser.find_element_by_css_selector(".regBtn").click()
    commonFunctions.wait_for_element(authorisation_form_checkpoint)
    browser.refresh()
    commonFunctions.wait_for_element(authorisation_form_checkpoint)


def admin_logout():
    browser.find_element_by_xpath("/html/body/div[1]/header/nav/div/ul/li/a/span").click()
    sleep(1)


def open_admin_socialite():
    browser.get("https://sback.nuxbet.com/")
    browser.set_window_size(1086, 1020)
    sleep(2)
    browser.find_element_by_xpath("//input[@type='email']").send_keys("admin_test@nuxbet.com")
    browser.find_element_by_xpath("//input[@type='password']").send_keys(config.PASSWORD)
    browser.find_element_by_xpath("//button[@type='submit']").click()
    sleep(1)
    browser.find_element_by_xpath("/html/body/div[1]/aside/section/ul/li[9]/a").click()
    sleep(1)
    browser.find_element_by_xpath("/html/body/div[1]/aside/section/ul/li[9]/ul/li[7]/a").click()
    sleep(1)


def social_network_check(social_network_name, networks_ui_basik_statement):
    try:
        browser.find_element_by_xpath(f"//img[@alt = '{social_network_name}']")
        networks_ui_basik_statement[f"{social_network_name}"] = "On"
    except NoSuchElementException:
        networks_ui_basik_statement[f"{social_network_name}"] = "Off"


def social_networks_statement_check_ui(networks_ui_basik_statement):
    # тут заполняем social_networks_ui_basic_statement
    commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    authorisation_form_open()
    sleep(2)
    for network_ui_basic_statement in networks_ui_basik_statement.keys():
        social_network_check(network_ui_basic_statement, networks_ui_basik_statement)
    browser.save_screenshot(f"{config.SCREENSHOT_PATH_AUTHORISATION}BasicSocialUISFront1Nuxbet.png")
    return networks_ui_basik_statement


def social_networks_admin_basic_statement_check(networks_ui_basik_statement, networks_admin_basik_statement):
    open_admin_socialite()
    for field_name in networks_ui_basik_statement.keys():
        networks_admin_basik_statement[f"{field_name} client_id"] = str(
            browser.find_element_by_name(f"social_id_{field_name}").get_attribute("value"))
        networks_admin_basik_statement[f"{field_name} client_secret"] = str(
            browser.find_element_by_name(f"social_secret_{field_name}").get_attribute("value"))
    admin_logout()
    return networks_admin_basik_statement


def social_networks_basik_comparison(networks_ui_basik_statement, networks_admin_basik_statement):
    for social_network_basic_statement_item in networks_ui_basik_statement.keys():
        if networks_ui_basik_statement.get(social_network_basic_statement_item) == "On":
            if networks_admin_basik_statement.get(
                    f"{social_network_basic_statement_item} client_id") == "" or\
                    networks_admin_basik_statement.get(
                        f"{social_network_basic_statement_item} client_secret") == "":
                print(f"{social_network_basic_statement_item} UI Error")
        if networks_ui_basik_statement.get(social_network_basic_statement_item) == "Off":
            if networks_admin_basik_statement.get(
                    f"{social_network_basic_statement_item} client_id") != "" and\
                    networks_admin_basik_statement.get(
                        f"{social_network_basic_statement_item} client_secret") != "":
                print(f"{social_network_basic_statement_item} UI Error")


def social_networks_turn_on(networks_ui_basik_statement, networks_ui_current_statement):
    for social_network_ui_basic_statement_item in networks_ui_basik_statement:
        networks_ui_current_statement[social_network_ui_basic_statement_item] = networks_ui_basik_statement.get(
                social_network_ui_basic_statement_item)
    open_admin_socialite()
    for key_of_social_network_current_statement_item in networks_ui_current_statement.keys():
        if networks_ui_current_statement[key_of_social_network_current_statement_item] == "Off":
            browser.find_element_by_name(f"social_id_{key_of_social_network_current_statement_item}").send_keys(
                f"TestID{key_of_social_network_current_statement_item}")
            browser.find_element_by_name(f"social_secret_{key_of_social_network_current_statement_item}").send_keys(
                f"TestSec{key_of_social_network_current_statement_item}")
            networks_ui_current_statement[key_of_social_network_current_statement_item] = "On"
    browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/button").click()
    sleep(2)
    browser.find_element_by_xpath("/html/body/div/header/nav/div/ul/li/a/span").click()
    commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    # auth_open()
    for key_of_social_networks_current_statement_item in networks_ui_current_statement.keys():
        try:
            browser.find_element_by_xpath(f"//img[@alt = '{key_of_social_networks_current_statement_item}']")
            print(f"{key_of_social_networks_current_statement_item} on, OK")
        except Exception as e:
            print(f"{key_of_social_networks_current_statement_item} on, NotOK, Error{e}")
    browser.save_screenshot(f"{config.SCREENSHOT_PATH_AUTHORISATION}SocNetwONSFront1Nuxbet.png")
    return networks_ui_current_statement


def social_networks_turn_off(networks_ui_current_statement):
    open_admin_socialite()
    for item_of_social_networks_current_statement in networks_ui_current_statement.keys():
        if networks_ui_current_statement[item_of_social_networks_current_statement] == "On":
            browser.find_element_by_name(f"social_id_{item_of_social_networks_current_statement}").send_keys(
                Keys.CONTROL + "a")
            browser.find_element_by_name(
                f"social_id_{item_of_social_networks_current_statement}").send_keys(Keys.DELETE)
            browser.find_element_by_name(f"social_secret_{item_of_social_networks_current_statement}").send_keys(
                Keys.CONTROL + "a")
            browser.find_element_by_name(f"social_secret_{item_of_social_networks_current_statement}").send_keys(
                Keys.DELETE)
            networks_ui_current_statement[item_of_social_networks_current_statement] = "Off"
    browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/button").click()
    sleep(2)
    browser.find_element_by_xpath("/html/body/div/header/nav/div/ul/li/a/span").click()
    commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    # auth_open()
    for item_of_current_statement_social_networks_list in networks_ui_current_statement.keys():
        try:
            browser.find_element_by_xpath(f"//img[@alt = '{item_of_current_statement_social_networks_list}']")
            print(f"{item_of_current_statement_social_networks_list} off, NotOK")
        except NoSuchElementException:  # ексепшн является позитив флоу, поэтому не описан
            print(f"{item_of_current_statement_social_networks_list} off, OK")
    browser.save_screenshot(f"{config.SCREENSHOT_PATH_AUTHORISATION}SocNetwOFFSFront1Nuxbet.png")
    return networks_ui_current_statement


def social_networks_set_to_default(networks_admin_basik_statement, networks_ui_basik_statement):
    open_admin_socialite()
    for key_of_basic_social_network_statement in networks_ui_basik_statement.keys():
        if networks_ui_basik_statement[key_of_basic_social_network_statement] == "On":
            browser.find_element_by_name(
                f"social_id_{key_of_basic_social_network_statement}"
            ).send_keys(networks_admin_basik_statement.get(f"{key_of_basic_social_network_statement} client_id"))
            browser.find_element_by_name(f"social_secret_{key_of_basic_social_network_statement}").send_keys(
                networks_admin_basik_statement.get(f"{key_of_basic_social_network_statement} client_secret"))
    browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/button").click()
    sleep(2)
    commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    sleep(1)
    browser.save_screenshot(f"{config.SCREENSHOT_PATH_AUTHORISATION}ToNormalStatementSFront1Nuxbet.png")


def social_networks_log_in(networks_ui_basik_statement):
    commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    # auth_open()
    for key_of_social_networks_statement_list in networks_ui_basik_statement.keys():
        if key_of_social_networks_statement_list != "vkontakte":
            browser.find_element_by_xpath(f"//img[@alt='{key_of_social_networks_statement_list}']").click()
            sleep(2)
            if browser.page_source.find("Some problems with captcha") > 0:
                print(f"{key_of_social_networks_statement_list} follow, Capcha")
            else:
                if browser.current_url != "https://sfront1.nuxbet.com/":
                    print(f"{key_of_social_networks_statement_list} follow, OK")
                else:
                    print(f"{key_of_social_networks_statement_list} follow, NotOK")
            sleep(1)
            browser.refresh()
            commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)


def gmail_login():
    browser.get("https://www.google.com/?gws_rd=ssl")
    browser.find_element_by_xpath("/html/body/div[1]/div[1]/div/div/div/div[2]/a").click()
    browser.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span"
        "/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(config.DEFAULT_MAIL)
    browser.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
    sleep(2)
    browser.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/"
        "div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input").send_keys(config.PASSWORD)
    browser.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
    commonFunctions.open_page(config.SFRONT1_SITE, main_page_checkpoint)
    sleep(2)
    try:
        browser.find_element_by_xpath("//div[@class='formWrap authForm']")
    except NoSuchElementException:  # тут ексепшн используется как логическое ветвление, поэтому не описан
        authorisation_form_open()
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[6]/div/a[2]/img"
                                  ).click()
    sleep(2)
    if browser.current_url != "https://sfront1.nuxbet.com/":
        if browser.page_source.find("nuxbetchk@gmail.com") > 0:
            browser.find_element_by_xpath("//div/ul/li[1]/div").click()
            browser.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/"
                "div/div[2]/div[1]/div/div/div/div/div[1]/div/div[1]/input").send_keys(config.PASSWORD)
            browser.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/"
                "span").click()
            sleep(1)
        else:
            sleep(2)
            browser.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/"
                "div[1]/div/div[1]/div/div[1]/input").send_keys(
                "nuxbetchk@gmail.com")
            browser.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/"
                "div[1]/div/div[1]/div/div[1]/input").send_keys(Keys.ENTER)
            sleep(1)  # нужно чтоб форма гугла обновилась
            browser.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input").send_keys(config.PASSWORD)
            sleep(1)
            browser.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input").send_keys(Keys.ENTER)
    commonFunctions.wait_for_element(main_page_checkpoint)
    sleep(3)
    if browser.page_source.find("109693494692241829544") > 0:
        print("google login, OK")
    else:
        print("google login, NotOK")


def general_check():
    social_networks_ui_basik_statement = {
        "facebook": "Off", "google": "Off", "linkedin": "Off", "twitter": "Off", "apple": "Off", "vkontakte": "Off"}
    social_networks_ui_current_statement = {
        "facebook": "Off", "google": "Off", "linkedin": "Off", "twitter": "Off", "apple": "Off", "vkontakte": "Off"}
    social_networks_admin_basik_statement = {
        "facebook client_id": "", "facebook client_secret": "", "google client_id": "", "google client_secret": "",
        "linkedin client_id": "", "linkedin client_secret": "", "twitter client_id": "", "twitter client_secret": "",
        "apple client_id": "", "apple client_secret": "", "vkontakte client_id": "", "vkontakte client_secret": ""}

    social_networks_ui_basik_statement = social_networks_statement_check_ui(social_networks_ui_basik_statement)
    social_networks_admin_basik_statement = social_networks_admin_basic_statement_check(
        social_networks_ui_basik_statement, social_networks_admin_basik_statement)
    social_networks_basik_comparison(social_networks_ui_basik_statement, social_networks_admin_basik_statement)
    social_networks_ui_current_statement = social_networks_turn_on(
        social_networks_ui_basik_statement, social_networks_ui_current_statement)
    social_networks_log_in(social_networks_ui_basik_statement)
    social_networks_turn_off(social_networks_ui_current_statement)
    social_networks_set_to_default(social_networks_admin_basik_statement, social_networks_ui_basik_statement)
    gmail_login()


general_check()
browser.close()
