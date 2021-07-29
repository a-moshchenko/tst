from datetime import datetime


def screenshot(func):
    def wrapper(browser, creds):
        try:
            func(browser, creds)
        except Exception as e:
            browser.get_screenshot(f'screenshots/{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.png')
            raise
    return wrapper

