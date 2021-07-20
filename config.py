from pathlib import Path
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# универсальные данные
EXECUTABLE_PATH = Path.cwd()/'driwers'/'chromedriver.exe'  # Тут указать путь к файлу драйвера браузера
PASSWD = "secretZ1"
ADMIN_PASSWORD = "secretZ13"

# данные для проверок коэфициентов
COEFPAGE = "https://dev.nuxbet.com/pre-match?sport_id="
COEFPAGEPROD = "https://nuxbet.com/pre-match?sport_id="
COEFLIVEPAGEPROD = "https://nuxbet.com/live?sport_id="
COEFLIVEPAGE = "https://dev.nuxbet.com/live?sport_id="
SCREENSHOTPATH = Path.cwd()/'screenshots'/'coef'

# данные для логина и авторизации
SITE = "https://dev.nuxbet.com/"  # url сайта, на котором будем проводить тест
SITE_PROD = "https://nuxbet.com/"
REFERAL_CODE = "QwERty123!@#"
AUTHORISATION_NAME = "autotestuser1672@mail.com"
PASSWORD = "secretZ1"
AUTHORISATION_NAME_EXIST = "autotestuser1672@mail.com" # мейл существующего пользователя
DEFAULT_MAIL = "nuxbetchk@gmail.com"
SFRONT1_SITE = "https://sfront1.nuxbet.com/"
AUTHORISATION_SHORT_NAME = "autotestuser1672"
SFRONT3_SITE = "https://sfront3.nuxbet.com/"
SCREENSHOT_PATH_AUTHORISATION = Path.cwd()/'screenshots'/f"{current_date}"
ADMIN_SFRONT3 = "https://sback.nuxbet.com/"

