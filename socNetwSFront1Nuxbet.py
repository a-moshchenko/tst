from time import sleep
import random
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config

# Перед запуском, по возможности, отключить капчу
print("Перед запуском, по возможности, отключить капчу")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH, options=chrome_options)
browser.set_window_size(1086, 1020)
current_date = date.today()
data = current_date.strftime("%d,%m,%Y")
screenshot_path = config.SCREENSHOTPATHAUTH
main_page_checkpoint = "/html/body/div/div[2]/div/section[2]/div"
authorisation_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"
social_networks_ui_basik_statement = {
    "facebook": "Off", "google": "Off", "linkedin": "Off", "twitter": "Off", "apple": "Off", "vkontakte": "Off"}
social_networks_ui_current_statement = {
    "facebook": "Off", "google": "Off", "linkedin": "Off", "twitter": "Off", "apple": "Off", "vkontakte": "Off"}
social_networks_admin_basik_statement = {
    "facebook client_id": "", "facebook client_secret": "", "google client_id": "", "google client_secret": "",
    "linkedin client_id": "", "linkedin client_secret": "", "twitter client_id": "", "twitter client_secret": "",
    "apple client_id": "", "apple client_secret": "", "vkontakte client_id": "", "vkontakte client_secret": ""}


def random_four_digits_number():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for i in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits


user_name = f"autotestuser{random_four_digits_number()}"


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"registration form open, Error, {e}")
        browser.close()


def authorisation_form_open():
    sleep(3)
    browser.find_element_by_css_selector(".regBtn").click()
    wait_for_element(authorisation_form_checkpoint)
    browser.refresh()
    wait_for_element(authorisation_form_checkpoint)


def open_main_page():
    browser.get(config.SFRONT1SITE)
    wait_for_element(main_page_checkpoint)
    browser.refresh()
    sleep(2)


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


def social_network_check(social_network_name):
    try:
        browser.find_element_by_xpath(f"//img[@alt = '{social_network_name}']")
        social_networks_ui_basik_statement[f"{social_network_name}"] = "On"
    except Exception:  # cама функция не должна ничего выводить, поэтому ексепшн не описан
        social_networks_ui_basik_statement[f"{social_network_name}"] = "Off"


def social_networks_statement_check_ui():
    # тут заполняем social_networks_ui_basic_statement
    open_main_page()
    authorisation_form_open()
    sleep(2)
    for i in social_networks_ui_basik_statement.keys():
        social_network_check(i)
    browser.save_screenshot(f"{current_date}BasicSocialUISFront1Nuxbet.png")
    return social_networks_ui_basik_statement


def social_networks_admin_basic_statement_check():
    open_admin_socialite()
    for field_name in social_networks_ui_basik_statement.keys():
        social_networks_admin_basik_statement[f"{field_name} client_id"] = str(
            browser.find_element_by_name(f"social_id_{field_name}").get_attribute("value"))
        social_networks_admin_basik_statement[f"{field_name} client_secret"] = str(
            browser.find_element_by_name(f"social_secret_{field_name}").get_attribute("value"))
    admin_logout()
    return social_networks_admin_basik_statement


def social_networks_basik_comparison():
    for i in social_networks_ui_basik_statement.keys():
        if social_networks_ui_basik_statement.get(i) == "On":
            if social_networks_admin_basik_statement.get(
                    f"{i} client_id") == "" or social_networks_admin_basik_statement.get(f"{i} client_secret") == "":
                print(f"{i} UI Error")
        if social_networks_ui_basik_statement.get(i) == "Off":
            if social_networks_admin_basik_statement.get(
                    f"{i} client_id") != "" and social_networks_admin_basik_statement.get(f"{i} client_secret") != "":
                print(f"{i} UI Error")


def social_networks_turn_on():
    for i in social_networks_ui_basik_statement:
        social_networks_ui_current_statement.update({i: social_networks_ui_basik_statement.get(i)})
    open_admin_socialite()
    for i in social_networks_ui_current_statement.keys():
        if social_networks_ui_current_statement[i] == "Off":
            browser.find_element_by_name(f"social_id_{i}").send_keys(f"TestID{i}")
            browser.find_element_by_name(f"social_secret_{i}").send_keys(f"TestSec{i}")
            social_networks_ui_current_statement[i] = "On"
    browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/button").click()
    sleep(2)
    browser.find_element_by_xpath("/html/body/div/header/nav/div/ul/li/a/span").click()
    open_main_page()
    # auth_open()
    for i in social_networks_ui_current_statement.keys():
        try:
            browser.find_element_by_xpath(f"//img[@alt = '{i}']")
            print(f"{i} on, OK")
        except Exception as e:
            print(f"{i} on, NotOK, Error{e}")
    browser.save_screenshot(f"{current_date}SocNetwONSFront1Nuxbet.png")
    return social_networks_ui_current_statement


def social_networks_turn_off():
    open_admin_socialite()
    for i in social_networks_ui_current_statement.keys():
        if social_networks_ui_current_statement[i] == "On":
            browser.find_element_by_name(f"social_id_{i}").send_keys(Keys.CONTROL + "a")
            browser.find_element_by_name(f"social_id_{i}").send_keys(Keys.DELETE)
            browser.find_element_by_name(f"social_secret_{i}").send_keys(Keys.CONTROL + "a")
            browser.find_element_by_name(f"social_secret_{i}").send_keys(Keys.DELETE)
            social_networks_ui_current_statement[i] = "Off"
    browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/button").click()
    sleep(2)
    browser.find_element_by_xpath("/html/body/div/header/nav/div/ul/li/a/span").click()
    open_main_page()
    # auth_open()
    for i in social_networks_ui_current_statement.keys():
        try:
            browser.find_element_by_xpath(f"//img[@alt = '{i}']")
            print(f"{i} off, NotOK")
        except Exception:  # ексепшн является позитив флоу, поэтому не описан
            print(f"{i} off, OK")
    browser.save_screenshot(f"{current_date}SocNetwOFFSFront1Nuxbet.png")
    return social_networks_ui_current_statement


def social_networks_set_to_default():
    open_admin_socialite()
    for i in social_networks_ui_basik_statement.keys():
        if social_networks_ui_basik_statement[i] == "On":
            browser.find_element_by_name(f"social_id_{i}").send_keys(social_networks_admin_basik_statement.get(
                f"{i} client_id"))
            browser.find_element_by_name(f"social_secret_{i}").send_keys(
                social_networks_admin_basik_statement.get(f"{i} client_secret"))
    browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/button").click()
    sleep(2)
    open_main_page()
    sleep(1)
    # auth_open()
    sleep(1)
    browser.save_screenshot(f"{current_date}ToNormalStatementSFront1Nuxbet.png")


def social_networks_log_in():
    open_main_page()
    # auth_open()
    for i in social_networks_ui_basik_statement.keys():
        if i != "vkontakte":
            browser.find_element_by_xpath(f"//img[@alt='{i}']").click()
            sleep(2)
            if browser.page_source.find("Some problems with captcha") > 0:
                print(f"{i} follow, Capcha")
            else:
                if browser.current_url != "https://sfront1.nuxbet.com/":
                    print(f"{i} follow, OK")
                else:
                    print(f"{i} follow, NotOK")
            sleep(1)
            browser.refresh()
            open_main_page()


def gmail_login():
    browser.get("https://www.google.com/?gws_rd=ssl")
    browser.find_element_by_xpath("/html/body/div[1]/div[1]/div/div/div/div[2]/a").click()
    browser.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span"
        "/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(config.DEFAULTMAIL)
    browser.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
    sleep(2)
    browser.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/"
        "div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input").send_keys(config.PASSWORD)
    browser.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
    open_main_page()
    sleep(2)
    try:
        browser.find_element_by_xpath("//div[@class='formWrap authForm']")
    except Exception:  # тут ексепшн используется как логическое ветвление, поэтому не описан
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
    wait_for_element(main_page_checkpoint)
    sleep(3)
    if browser.page_source.find("109693494692241829544") > 0:
        print("google login, OK")
    else:
        print("google login, NotOK")


social_networks_ui_basik_statement = social_networks_statement_check_ui()  # переменная используется выше
social_networks_admin_basik_statement = social_networks_admin_basic_statement_check()  # переменная используется выше
social_networks_basik_comparison()
social_networks_ui_current_statement = social_networks_turn_on()  # переменная используется выше
social_networks_log_in()
social_networks_turn_off()
social_networks_set_to_default()
gmail_login()
browser.close()
