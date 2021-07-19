from time import sleep
from selenium import webdriver
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import config

browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH)
browser.set_window_size(1086, 1020)
current_date = date.today()
date = current_date.strftime("%d,%m,%Y")
screenshot_path = config.SCREENSHOTPATHAUTH
main_page_checkpoint = "/html/body/div/div[2]/div/section[4]/header"
login_form_checkpoint = "/html/body/div/div[1]/div[2]/div/div/div/div"
login_button_checkpoint = "/html/body/div/nav/div/a[2]"
print("check, result")


def wait_for_element(xpath):
    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print(f"page open, Error, {e}")


def open_main_page():
    browser.get(config.SITE)
    wait_for_element(main_page_checkpoint)


def login():
    open_main_page()
    login_button = browser.find_element_by_xpath("/html/body/div/div[1]/div/div/div[2]/div[3]/a")
    login_button.click()
    try:
        browser.find_element_by_css_selector(".formHeader")
        print("auth form, OK")
    except Exception as e:
        print(f"auth form, NotOK, {e}")
    forgot_password_button = browser.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/div/div/div/div/form/div[1]/div[2]/div[2]")
    forgot_password_button.click()
    wait_for_element(login_form_checkpoint)
    browser.save_screenshot(f"{screenshot_path}ForgotPasswordFormNuxbetDewNuxbet.png")
    print("forgot password form, OK")
    send_button = browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div[2]")
    send_button.click()
    sleep(1)  # слип нужен чтоб дать форме обновиться
    if str(browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/input"
                                         ).get_attribute("class")) == "inputError":
        browser.save_screenshot(f"{screenshot_path}NoMailWarningPasswordRecoveryFormDewNuxbet.png")
        print("no email, OK")
    else:
        print("no email, NotOK")
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[2]/span[2]").click()
    wait_for_element(login_button_checkpoint)
    if browser.current_url == "https://dev.nuxbet.com/tickets/create":
        browser.save_screenshot(f"{screenshot_path}ContactUsDewNuxbet.png")
        print("contact us, OK")
    else:
        print("contact us, NotOK")

    login_button = browser.find_element_by_xpath("//div[3]/a")  # ввод несуществующей почты
    login_button.click()
    forgot_password_button = browser.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/div/div/div/div/form/div[1]/div[2]/div[2]")
    forgot_password_button.click()
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/input"
                                  ).send_keys("invalidmail@mail.com")
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div[2]/button").click()
    if browser.page_source.find("We have sent a verification code to your email.") > 0:
        browser.save_screenshot(f"{screenshot_path}SecurityCodeDewNuxbet.png")
        print("security code sent, OK")
    else:
        print("security code sent, OK")
    sleep(1)
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[1]/button").click()
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/div[1]/button").click()
    browser.get(config.SITE+"tickets/create")
    sleep(1)
    user_name = browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div[1]/input")
    user_name.click()
    user_name.send_keys("username")
    browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div[2]/input"
                                  ).send_keys("invalidmail@mail.com")
    browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div[3]/input").send_keys("test_ticket")
    browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div[4]/textarea"
                                  ).send_keys("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
                                              "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim "
                                              "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea"
                                              " commodo consequat.")
    sleep(1)
    browser.find_element_by_xpath("/html/body/div/div[2]/div/section/div/form/div[6]/button[1]").click()
    sleep(2)  # ожидание не всегда корректно отрабатывает. тут надежнее слип
    if browser.page_source.find("Thanks in advance for your patience!") > 0:
        browser.save_screenshot(f"{screenshot_path}TicketCreatedDewNuxbet.png")
        print("ticket, OK")
    else:
        print("ticket, NotOK")

    login_button = browser.find_element_by_xpath("//div[3]/a")  # ввод невалидной почты
    login_button.click()
    forgot_password_button = browser.find_element_by_xpath(
        "/html/body/div/div[1]/div[2]/div/div/div/div/form/div[1]/div[2]/div[2]")
    forgot_password_button.click()
    sleep(1)
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/input").send_keys("invalidmail")
    browser.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div/form/div[2]/button").click()
    sleep(1)  # ждем пока форма обновится
    if browser.page_source.find("Your password cannot be recovered, contact support.") > 0:
        browser.save_screenshot(f"{screenshot_path}TicketNotCreatedDewNuxbet.png")
        print("invalid mail message, OK")
    else:
        print("invalid mail message, NotOK")


login()
browser.close()
