from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

EXECUTABLE_PATH = r"C:\chromedriver\chromedriver"  # Тут указать путь к файлу драйвера браузера
browser = webdriver.Chrome(executable_path=EXECUTABLE_PATH)

AUTHNAME = "autotestuser1672@mail.com"
PASSWORD = "secretZ1"


def open():
    site = "https://dev.nuxbet.com/"
    browser.get(site)
    browser.set_window_size(1086, 1020)
    sleep(2)


def login_opn():
    login_btn_main = browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/button")
    login_btn_main.click()


def general_run():
    open()
    login_opn()
    sleep(1)
    browser.find_element_by_xpath("//input[@type='text']").send_keys(
        AUTHNAME)  # вводим мейл пользователя
    browser.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(
        "LoremIpsum")  # вводим имя пользователя
    browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[4]/input").send_keys(
        PASSWORD)  # вводим пароль
    browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div/div/div[6]/input").send_keys(
        PASSWORD)  # подтверждаем пароль
    TC = browser.find_element_by_xpath(
        "/html/body/div/div[2]/div/section/div/form/div/div/input[4]")  # определяем элемент чкубокс terms&conditions
    browser.execute_script("arguments[0].click();", TC)  # соглашаемся с T&C
    for i in range(12):
        sleep(2)
        try:
            login_button = browser.find_element_by_xpath(
                "/html/body/div/div[2]/div/section/div/form/div/div/div[8]/button")
            login_button.click()
        except:
            print("Capcha, OK")
            break


general_run()
browser.close()
