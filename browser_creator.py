from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import config


class Driver:
    def __init__(self):
        options = Options()
        if config.DEBUG:
            options.headless = False
        else:
            options.headless = True
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(executable_path=config.EXECUTABLE_PATH,
                                        options=options)
        self.browser.set_window_size(1920, 1080)

    def screenshot(self, filename):
        self.browser.save_screenshot(filename)

    def quit(self):
        self.browser.quit()

    def go_to(self, url: str) -> None:
        self.browser.get(url)

    def _wait_elems(self, phrase: tuple, timeout: int = 5) -> WebDriverWait:
        return WebDriverWait(self.browser, timeout).until(ec.presence_of_all_elements_located(phrase))

    def get_screenshot(self, name: str) -> None:
        self.browser.get_screenshot_as_file(name)

    def switch_to_iframe(self, element):
        self.browser.switch_to.frame(element)

    def interaction_with(self, phrase, timeout=10, clickable=False, scroll=False, click=False, text=None):
        """ Функция взаимодействия с элементомами. Возвращает запрошенный элемент """
        # Дожидаемся появления элемента на странице
        elems = self._wait_elems(phrase, timeout)

        # Проверяем сколько элементов обнаружено
        if len(elems) > 1:
            # Если найдена группа элементов, то возвращаем список элементов
            return elems
        else:
            # Иначе - начинаем взаимодействие
            elem: object = elems[0]

        if clickable:
            # Дожидаемся кликабельности элемента
            WebDriverWait(self.browser, timeout).until(ec.element_to_be_clickable(phrase))

        if scroll:
            # Скроллим элемент в пределы видимости:
            elem.location_once_scrolled_into_view

        if click:
            # Нажимаем на элемент
            self.browser.execute_script("(arguments[0]).click();", elem)
        if text is not None:
            # Вводим текст
            elem.clear()
            elem.send_keys(text)

        return elem
