from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

ep = r"C:\chromedriver\chromedriver"  # Тут указать путь к файлу драйвера браузера
browser = webdriver.Chrome(executable_path=ep)

authname = "autotestuser1672@mail.com"

def open():
    site = "https://dev.nuxbet.com/"
    browser.get(site)
    browser.set_window_size(1086, 1020)
    sleep(2)

def close():
    # Закрывает окно браузера
    browser.close()

def logInOpn():
    logInBtnM = browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/button")
    logInBtnM.click()

def generalRun():
    open()
    logInOpn()
    sleep(1)
    (browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/input[1]")).send_keys("autotestuser1672@mail.com")
    (browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/input[2]")).send_keys("LoremIpsum")
    (browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[4]/input")).send_keys("secretZ1")
    (browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[6]/input")).send_keys("secretZ1")
    tc = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/input[4]")
    browser.execute_script("arguments[0].click();", tc)
    for i in range(12):
        sleep(1)
        #print("iter, ", i)
        try:
            logBtn = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
            logBtn.click()
        except:
            print("Capcha, OK")
            break




generalRun()