# Перед запуском, по возможности, отключить капчу
print("Перед запуском, по возможности, отключить капчу")

from time import sleep
import random
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH, options=chrome_options)
current_date = date.today()
data = current_date.strftime("%d,%m,%Y")
social_networks_ui_basik_statement = {"facebook":"Off", "google":"Off", "linkedin":"Off", "twitter":"Off", "apple":"Off", "vkontakte":"Off"}
social_networks_ui_current_statement = {"facebook":"Off", "google":"Off", "linkedin":"Off", "twitter":"Off", "apple":"Off", "vkontakte":"Off"}
social_networks_admin_basik_statement = {"facebook client_id":"", "facebook client_secret":"", "google client_id":"", "google client_secret":"", "linkedin client_id":"", "linkedin client_secret":"", "twitter client_id":"", "twitter client_secret":"", "apple client_id":"", "apple client_secret":"", "vkontakte client_id":"", "vkontakte client_secret":""}

def randnum():
    # генерит рандомную строку из четырех цыфр
    random_four_digits = ""
    for i in range(4):
        random_four_digits += str(random.randint(1, 9))
    return random_four_digits

user_name = f"autotestuser{randnum()}"

def auth_open():
    sleep(3)
    browser.find_element_by_css_selector(".regBtn").click()
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div[2]/div/div/div/div"))
        )
    except:
        print("registr form open, Error")
        browser.close()
    browser.refresh()
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div[2]/div/div/div/div"))
        )
    except:
        print("registr form open, Error")
        browser.close()

def open():
    browser.get(config.SFRONT1SITE)
    browser.set_window_size(1086, 1020)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/section[2]/div"))
        )
    except:
        print("page open, Error")
        browser.close()
    browser.refresh()
    sleep(2)

def admmin_logout():
    browser.find_element_by_xpath("/html/body/div[1]/header/nav/div/ul/li/a/span").click()
    sleep(1)

def open_admin_socialite():
    browser.get("https://sback.nuxbet.com/")
    browser.set_window_size(1086, 1020)
    sleep(1)
    browser.find_element_by_xpath("/html/body/div/div/div/form/div[1]/input").send_keys("admin_test@nuxbet.com")
    browser.find_element_by_xpath("/html/body/div/div/div/form/div[1]/div[3]/input").send_keys("secretZ1")
    browser.find_element_by_xpath("/html/body/div/div/div/form/div[2]/button").click()
    sleep(1)
    browser.find_element_by_xpath("/html/body/div[1]/aside/section/ul/li[9]/a").click()
    sleep(1)
    browser.find_element_by_xpath("/html/body/div[1]/aside/section/ul/li[9]/ul/li[7]/a").click()
    sleep(1)

def social_networks_statement_check_UI():
    # тут заполняем social_networks_ui_basic_statement
    open()
    auth_open()
    sleep(2)
    if str(browser.page_source).find("facebook.png") > 0:
        social_networks_ui_basik_statement["facebook"] = "On"
    if str(browser.page_source).find("google.png") > 0:
        social_networks_ui_basik_statement["google"] = "On"
    if str(browser.page_source).find("linkedin.png") > 0:
        social_networks_ui_basik_statement["linkedin"] = "On"
    if str(browser.page_source).find("twitter.png") > 0:
        social_networks_ui_basik_statement["twitter"] = "On"
    if str(browser.page_source).find("apple.png") > 0:
        social_networks_ui_basik_statement["apple"] = "On"
    if str(browser.page_source).find("vk.png") > 0:
        social_networks_ui_basik_statement["vkontakte"] = "On"
    browser.save_screenshot(str(current_date)+"BasicSocialUISFront1Nuxbet.png")
    return social_networks_ui_basik_statement

def social_networks_admin_basik_statement_check():
    open_admin_socialite()
    social_networks_admin_basik_statement["facebook client_id"] = str(browser.find_element_by_xpath(
        "/html/body/div/div/section[2]/div/div/div/div[2]/form/div[1]/input").get_attribute("value"))
    social_networks_admin_basik_statement["facebook client_secret"] = str(browser.find_element_by_xpath(
        "/html/body/div/div/section[2]/div/div/div/div[2]/form/div[2]/input").get_attribute("value"))
    social_networks_admin_basik_statement["google client_id"] =  str(browser.find_element_by_xpath(
        "/html/body/div/div/section[2]/div/div/div/div[2]/form/div[4]/input").get_attribute("value"))
    social_networks_admin_basik_statement["google client_secret"] = str(browser.find_element_by_xpath(
        "/html/body/div/div/section[2]/div/div/div/div[2]/form/div[5]/input").get_attribute("value"))
    social_networks_admin_basik_statement["linkedin client_id"] = str(browser.find_element_by_xpath(
        "/html/body/div/div/section[2]/div/div/div/div[2]/form/div[7]/input").get_attribute("value"))
    social_networks_admin_basik_statement["linkedin client_secret"] = str(browser.find_element_by_xpath(
        "/html/body/div/div/section[2]/div/div/div/div[2]/form/div[8]/input").get_attribute("value"))
    social_networks_admin_basik_statement["twitter client_id"] = str(browser.find_element_by_xpath(
        "/html/body/div/div/section[2]/div/div/div/div[2]/form/div[10]/input").get_attribute("value"))
    social_networks_admin_basik_statement["twitter client_secret"] = str(browser.find_element_by_xpath(
        "/html/body/div/div/section[2]/div/div/div/div[2]/form/div[11]/input").get_attribute("value"))
    social_networks_admin_basik_statement["apple client_id"] = str(browser.find_element_by_xpath(
        "/html/body/div/div/section[2]/div/div/div/div[2]/form/div[13]/input").get_attribute("value"))
    social_networks_admin_basik_statement["apple client_secret"] = str(browser.find_element_by_xpath(
        "/html/body/div/div/section[2]/div/div/div/div[2]/form/div[14]/input").get_attribute("value"))
    social_networks_admin_basik_statement["vkontakte client_id"] = str(browser.find_element_by_xpath(
        "/html/body/div/div/section[2]/div/div/div/div[2]/form/div[16]/input").get_attribute("value"))
    social_networks_admin_basik_statement["vkontakte client_secret"] = str(browser.find_element_by_xpath(
        "/html/body/div/div/section[2]/div/div/div/div[2]/form/div[17]/input").get_attribute("value"))
    browser.find_element_by_xpath("/html/body/div/header/nav/div/ul/li/a/span").click()
    return social_networks_admin_basik_statement

def social_networks_basik_comparison():
    if social_networks_ui_basik_statement.get("facebook") == "On":
        if social_networks_admin_basik_statement.get("facebook client_id") == "" or social_networks_admin_basik_statement.get("facebook client_secret") == "":
            print("facebook UI Error")
    if social_networks_ui_basik_statement.get("google") == "On":
        if social_networks_admin_basik_statement.get("google client_id") == "" or social_networks_admin_basik_statement.get("google client_secret") == "":
            print("google UI Error")
    if social_networks_ui_basik_statement.get("linkedin") == "On":
        if social_networks_admin_basik_statement.get("linkedin client_id") == "" or social_networks_admin_basik_statement.get("linkedin client_secret") == "":
            print("linkedin UI Error")
    if social_networks_ui_basik_statement.get("twitter") == "On":
        if social_networks_admin_basik_statement.get("twitter client_id") == "" or social_networks_admin_basik_statement.get("twitter client_id") == "":
            print("twitter UI Error")
    if social_networks_ui_basik_statement.get("apple") == "On":
        if social_networks_admin_basik_statement.get("apple client_id") == "" or social_networks_admin_basik_statement.get("apple client_id") == "":
            print("apple UI Error")
    if social_networks_ui_basik_statement.get("vkontakte") == "On":
        if social_networks_admin_basik_statement.get("vkontakte client_id") == "" or social_networks_admin_basik_statement.get("vkontakte client_id") == "":
            print("vkontakte UI Error")
        else:
            print("basic comparison, OK")

def social_networks_turn_on():
    for i in social_networks_ui_basik_statement:
        social_networks_ui_current_statement.update({i:social_networks_ui_basik_statement.get(i)})

    open_admin_socialite()
    if social_networks_ui_current_statement.get("facebook") == "Off" :
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[1]/input").send_keys("TestIDFb")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[2]/input").send_keys("TestSecFb")
        social_networks_ui_current_statement["facebook"] = "On"
    if social_networks_ui_current_statement.get("google") == "Off" :
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[4]/input").send_keys("TestIDG")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[5]/input").send_keys("TestSecG")
        social_networks_ui_current_statement["google"] = "On"
    if social_networks_ui_current_statement.get("linkedin") == "Off" :
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[7]/input").send_keys("TestIDLI")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[8]/input").send_keys("TestSecLI")
        social_networks_ui_current_statement["linkedin"] = "On"
    if social_networks_ui_current_statement.get("twitter") == "Off" :
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[10]/input").send_keys("TestIDTW")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[11]/input").send_keys("TestSecTW")
        social_networks_ui_current_statement["twitter"] = "On"
    if social_networks_ui_current_statement.get("apple") == "Off" :
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[13]/input").send_keys("TestIDAP")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[14]/input").send_keys("TestSecAP")
        social_networks_ui_current_statement["apple"] = "On"
    if social_networks_ui_current_statement.get("vkontakte") == "Off" :
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[16]/input").send_keys("TestIDAP")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[17]/input").send_keys("TestSecAP")
        social_networks_ui_current_statement["vkontakte"] = "On"
    browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/button").click()
    sleep(2)
    browser.find_element_by_xpath("/html/body/div/header/nav/div/ul/li/a/span").click()
    open()
    #auth_open()
    if str(browser.page_source).find("facebook.png") > 0:
        print("facebook on, OK")
    else:
        print("facebook on, NotOK")
    if str(browser.page_source).find("google.png") > 0:
        print("google on, OK")
    else:
        print("google on, NotOK")
    if str(browser.page_source).find("linkedin.png") > 0:
        print("linkedin on, OK")
    else:
        print("linkedin on, NotOK")
    if str(browser.page_source).find("twitter.png") > 0:
        print("twitter on, OK")
    else:
        print("twitter on, NotOK")
    if str(browser.page_source).find("apple.png") >0:
        print("apple on, OK")
    else:
        print("apple on, NotOK")
    if str(browser.page_source).find("vk.png") >0:
        print("vk on, OK")
    else:
        print("vk on, NotOK")
    browser.save_screenshot(str(f"{current_date}SocNetwONSFront1Nuxbet.png"))
    return social_networks_ui_current_statement

def social_networks_turn_off():
    open_admin_socialite()
    if social_networks_ui_current_statement.get("facebook") == "On":
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[1]/input").send_keys(Keys.CONTROL +"a")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[1]/input").send_keys(
            Keys.DELETE)
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[2]/input").send_keys(Keys.CONTROL +"a")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[2]/input").send_keys(
            Keys.DELETE)
        social_networks_ui_current_statement["facebook"] = "Off"
    if social_networks_ui_current_statement.get("google") == "On":
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[4]/input").send_keys(Keys.CONTROL +"a")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[4]/input").send_keys(
            Keys.DELETE)
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[5]/input").send_keys(Keys.CONTROL +"a")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[5]/input").send_keys(
            Keys.DELETE)
        social_networks_ui_current_statement["google"] = "Off"
    if social_networks_ui_current_statement.get("linkedin") == "On":
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[7]/input").send_keys(Keys.CONTROL +"a")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[7]/input").send_keys(
            Keys.DELETE)
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[8]/input").send_keys(Keys.CONTROL +"a")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[8]/input").send_keys(
            Keys.DELETE)
        social_networks_ui_current_statement["linkedin"] = "Off"
    if social_networks_ui_current_statement.get("twitter") == "On":
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[10]/input").send_keys(Keys.CONTROL +"a")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[10]/input").send_keys(
            Keys.DELETE)
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[11]/input").send_keys(Keys.CONTROL +"a")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[11]/input").send_keys(
            Keys.DELETE)
        social_networks_ui_current_statement["twitter"] = "Off"
    if social_networks_ui_current_statement.get("apple") == "On":
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[13]/input").send_keys(Keys.CONTROL +"a")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[13]/input").send_keys(
            Keys.DELETE)
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[14]/input").send_keys(Keys.CONTROL +"a")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[14]/input").send_keys(
            Keys.DELETE)
        social_networks_ui_current_statement["apple"] = "Off"
    if social_networks_ui_current_statement.get("vkontakte") == "On":
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[16]/input").send_keys(Keys.CONTROL +"a")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[16]/input").send_keys(
            Keys.DELETE)
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[17]/input").send_keys(Keys.CONTROL +"a")
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[17]/input").send_keys(
            Keys.DELETE)
        social_networks_ui_current_statement["vkontakte"] = "Off"
    browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/button").click()
    sleep(2)
    browser.find_element_by_xpath("/html/body/div/header/nav/div/ul/li/a/span").click()
    open()
    #auth_open()
    if str(browser.page_source).find("facebook.png") > 0:
        print("facebook off, NotOK")
    else:
        print("facebook off, OK")
    if str(browser.page_source).find("google.png") > 0:
        print("google off, NotOK")
    else:
        print("google off, OK")
    if str(browser.page_source).find("linkedin.png") > 0:
        print("linkedin off, NotOK")
    else:
        print("linkedin off, OK")
    if str(browser.page_source).find("twitter.png") > 0:
        print("twitter off, NotOK")
    else:
        print("twitter off, OK")
    if str(browser.page_source).find("apple.png") > 0:
        print("apple off, NotOK")
    else:
        print("apple off, OK")
    if str(browser.page_source).find("vk.png") > 0:
        print("vk off, NotOK")
    else:
        print("vk off, OK")
    browser.save_screenshot(str(f"{current_date}SocNetwOFFSFront1Nuxbet.png"))
    return social_networks_ui_current_statement

def social_networks_set_to_default():
    open_admin_socialite()
    if social_networks_ui_basik_statement.get("facebook") == "On":
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[1]/input").send_keys(
            social_networks_admin_basik_statement.get("facebook client_id"))
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[2]/input").send_keys(
            social_networks_admin_basik_statement.get("facebook client_secret"))
    if social_networks_ui_basik_statement.get("google") == "On":
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[4]/input").send_keys(
            social_networks_admin_basik_statement.get("google client_id"))
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[5]/input").send_keys(
            social_networks_admin_basik_statement.get("google client_secret"))
    if social_networks_ui_basik_statement.get("linkedin") == "On":
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[7]/input").send_keys(
            social_networks_admin_basik_statement.get("linkedin client_id"))
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[8]/input").send_keys(
            social_networks_admin_basik_statement.get("linkedin client_secret"))
    if social_networks_ui_basik_statement.get("twitter") == "On":
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[10]/input").send_keys(
            social_networks_admin_basik_statement.get("twitter client_id"))
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[11]/input").send_keys(
            social_networks_admin_basik_statement.get("twitter client_secret"))
    if social_networks_ui_basik_statement.get("apple") == "On":
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[13]/input").send_keys(
            social_networks_admin_basik_statement.get("apple client_id"))
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[14]/input").send_keys(
            social_networks_admin_basik_statement.get("apple client_secret"))
    if social_networks_ui_basik_statement.get("vkontakte") == "On":
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[16]/input").send_keys(
            social_networks_admin_basik_statement.get("vkontakte client_id"))
        browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/div[17]/input").send_keys(
            social_networks_admin_basik_statement.get("vkontakte client_secret"))
    browser.find_element_by_xpath("/html/body/div/div/section[2]/div/div/div/div[2]/form/button").click()
    sleep(2)
    open()
    sleep(1)
    #auth_open()
    sleep(1)
    browser.save_screenshot(str(f"{current_date}ToNormalStatementSFront1Nuxbet.png"))

def social_networks_log_in():
    open()
    #auth_open()
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[6]/div/a[1]/img").click()
    sleep(2)
    if str(browser.page_source).find("Some problems with captcha")>0:
        print("fb follow, Capcha")
    else:
        if str(browser.current_url) != "https://sfront1.nuxbet.com/":
            print("fb follow, OK")
        else:
            print("fb follow, NotOK")
    sleep(1)
    open()
    #auth_open()
    browser.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[6]/div/a[2]/img").click()
    sleep(2)
    if str(browser.page_source).find("Some problems with captcha")>0:
        print("google follow, Capcha")
    else:
        if str(browser.current_url) != "https://sfront1.nuxbet.com/":
            print("google follow, OK")
        else:
            print("google follow, NotOK")
    sleep(1)
    open()
    #auth_open()
    browser.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[6]/div/a[3]/img").click()
    sleep(2)
    if str(browser.page_source).find("Some problems with captcha")>0:
        print("linkedin follow, Capcha")
    else:
        if str(browser.current_url) != "https://sfront1.nuxbet.com/":
            print("linkedin follow, OK")
        else:
            print("linkedin follow, NotOK")
    sleep(1)
    open()
    #auth_open()
    browser.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[6]/div/a[4]/img").click()
    sleep(2)
    if str(browser.page_source).find("Some problems with captcha")>0:
        print("twitter follow, Capcha")
    else:
        if str(browser.current_url) != "https://sfront1.nuxbet.com/":
            print("twitter follow, OK")
        else:
            print("twitter follow, NotOK")
    sleep(1)
    open()
    #auth_open()
    browser.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[6]/div/a[5]/img").click()
    sleep(2)
    if str(browser.page_source).find("Some problems with captcha")>0:
        print("apple follow, Capcha")
    else:
        if str(browser.current_url) != "https://sfront1.nuxbet.com/":
            print("apple follow, OK")
        else:
            print("apple follow, NotOK")
    sleep(1)
    open()
    # разкомментить при запуске в ВПН
    #auth_open()
    #browser.find_element_by_xpath(
    #    "/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[6]/div/a[6]/img").click()
    #sleep(2)
    #if str(browser.current_url) != "https://sfront1.nuxbet.com/":
    #    print("vk follow, OK")
    #else:
    #    print("vk follow, NotOK")

def gmail_login():
    browser.get("https://www.google.com/?gws_rd=ssl")
    browser.find_element_by_xpath("/html/body/div[1]/div[1]/div/div/div/div[2]/a").click()
    browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys("nuxbetchk@gmail.com")
    browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
    sleep(2)
    browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input").send_keys("secretZ1")
    browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
    open()
    #auth_open()
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div/div/div[6]/div/a[2]/img").click()
    if str(browser.current_url) != "https://sfront1.nuxbet.com/":
        if str(browser.page_source).find("nuxbetchk@gmail.com")>0:
            browser.find_element_by_xpath("//div/ul/li[1]/div").click()
            browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/div[1]/input").send_keys("secretZ1")
            browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
        else:
            sleep(1)
            browser.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(
                "nuxbetchk@gmail.com")
            browser.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
    sleep(1)
    if str(browser.page_source).find("109693494692241829544")>0:
        print("google login, OK")
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/span[1]").click()
        sleep(1)
        browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/div[2]/a[7]").click()
    else:
        print("google login, NotOK")

social_networks_ui_basik_statement = social_networks_statement_check_UI()
social_networks_admin_basik_statement = social_networks_admin_basik_statement_check()
social_networks_basik_comparison()
social_networks_ui_current_statement = social_networks_turn_on()
social_networks_log_in()
social_networks_turn_off()
social_networks_set_to_default()
gmail_login()
browser.close()