from pathlib import Path
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium import webdriver

current_date = date.today()
screenshot_date = current_date.strftime("%Y-%m-%d")

# универсальные данные
EXECUTABLE_PATH = Path.cwd()/'driwers'/'chromedriver.exe'  # Тут указать путь к файлу драйвера браузера
PASSWD = "secretZ1"

# данные для проверок коэфициентов
COEFPAGE = "https://dev.nuxbet.com/pre-match?sport_id="
COEFPAGEPROD = "https://nuxbet.com/pre-match?sport_id="
COEFLIVEPAGEPROD = "https://nuxbet.com/live?sport_id="
COEFLIVEPAGE = "https://dev.nuxbet.com/live?sport_id="
SCREENSHOTPATH = f"{Path.cwd()}/'screenshots'/'coef'"

# данные для логина и авторизации
SITE = "https://dev.nuxbet.com/"  # url сайта, на котором будем проводить тест
REFCODE = "QwERty123!@#"
AUTHNAME = "autotestuser1672@mail.com"
PASSWORD = "secretZ1"
AUTH_NAME_EXIST = "autotestuser1672@mail.com" # мейл существующего пользователя
DEFAULTMAIL = "nuxbetchk@gmail.com"
SFRONT1SITE = "https://sfront1.nuxbet.com/"
AUTHSHORTNAME = "autotestuser1672"
SFRONT3SITE = "https://sfront3.nuxbet.com/"

SCREENSHOTPATHAUTH = f"{Path.cwd()}/'screenshots'/{date}"
ADMIN_PASSWORD = "secretZ13"
ABACK_HEADERS = {
    'authority': 'aback.nuxbet.com',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://aback.nuxbet.com/admin/bets/index',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'start=eyJpdiI6ImpOc01obGlMdjRuSXo2ZmhWZUlLRXc9PSIsInZhbHVlIjoiRlI1c3M3OEJlZGRheEtWNnJ4a1dBSG9qb1FPY1NkMDRMUW5KUWhTbXN4MGpnT2FYYjNycnVSWkloY3E5TThWc3lPMm42dkxJNVRvY1ZuSXZEZUwwVkE9PSIsIm1hYyI6IjU2YjYzMTI1N2QxZWYxN2RlNDkyMzQ3M2ViOTdiNGNiZWRhOTI2OGQxNTQ0OTMyZWRlNmZiY2Y0ZGNjNzA4NmQifQ%3D%3D; end=eyJpdiI6ImwyUTh5TEl6cU1YRXFDTnk1YmU3Snc9PSIsInZhbHVlIjoiSGtUZmdnZnIxbHFEWVJLVDVubHhGN0dFV2hyNTNmbm1FVjE1MDNmaHBNR0RGeE1ZWmlDMG5MMTgrQ1A0MnJjRllDYUVES00wQkR4OHVxTFd0UER3V2c9PSIsIm1hYyI6ImZkZDY2NzRjZDg4NGUwMzUwZmY1NGRiYTA2MmM3ZDU3YmUyNzczN2MyNjJkNTQ1MGUyYzVhNzI5Y2ZhYjAyMjMifQ%3D%3D; io=Er68u1OE5yXhJZywAADr; XSRF-TOKEN=eyJpdiI6IkZKTVl2dzhJRFZuNWlHNmdtVlVFMnc9PSIsInZhbHVlIjoiTW9xMW9Sd3l1V2tKN3A1RjJTM2ZTb0k4cTdXL2ZleEMxekRreEh3elliMTg1YW5IMTRST1JPQVJVZUFxNWY2Uk9pblBZSDdYeGRkdVBQZFhJSS9Lb2JiYm9ZL3d1bVlTbjZNemZvaGNDVlJZWUFaeHZpZmQ1c29ueDlqbHJHZ1AiLCJtYWMiOiIyNDQyMDIwOWM1ZDMzZmUzOGI3ZjQxMDVkMjA5NGM2Nzc4NDk5OTgxZmJiZGJjM2MwNGQwOWRiNjdmODQ3MDhkIn0%3D; nuxbet_session=eyJpdiI6Impaek05ZEhJS0w3dm1wUytsclZMZlE9PSIsInZhbHVlIjoiYXpvRkJrdUlqWTVndzErK1ZlUE5UZkw2Um1GbkdZS1JrRnk3M2NaOVpNK2pOdGRxTVJPQWVtTU13TXEzM2lKSDNaOUNvUnoyNmN4ZmRJZzFRVUhEVEVFSEVER2VqK3p5eHFOOFh4TG42VjEvdU5oQWVEK00waFF3djVNWlEveWsiLCJtYWMiOiIxNTUyMDA3MzZmYmMxMDI2ZTM4MTA0MGIyNDE5ZmYwYzBlNTM0ZDRjZTlkNzcxNjc4OGI1NzAxMDgxOWJiZWExIn0%3D',
}
ABACK_PARAMS = params = (
    ('draw', '1'),
    ('columns[0][data]', ''),
    ('columns[0][name]', ''),
    ('columns[0][searchable]', 'true'),
    ('columns[0][orderable]', 'false'),
    ('columns[0][search][value]', ''),
    ('columns[0][search][regex]', 'false'),
    ('columns[1][data]', 'id'),
    ('columns[1][name]', ''),
    ('columns[1][searchable]', 'true'),
    ('columns[1][orderable]', 'true'),
    ('columns[1][search][value]', ''),
    ('columns[1][search][regex]', 'false'),
    ('columns[2][data]', 'user'),
    ('columns[2][name]', ''),
    ('columns[2][searchable]', 'true'),
    ('columns[2][orderable]', 'true'),
    ('columns[2][search][value]', ''),
    ('columns[2][search][regex]', 'false'),
    ('columns[3][data]', 'created_at'),
    ('columns[3][name]', ''),
    ('columns[3][searchable]', 'true'),
    ('columns[3][orderable]', 'true'),
    ('columns[3][search][value]', f'{screenshot_date},{screenshot_date}'),
    ('columns[3][search][regex]', 'false'),
    ('columns[4][data]', 'type'),
    ('columns[4][name]', ''),
    ('columns[4][searchable]', 'true'),
    ('columns[4][orderable]', 'true'),
    ('columns[4][search][value]', ''),
    ('columns[4][search][regex]', 'false'),
    ('columns[5][data]', 'odds'),
    ('columns[5][name]', ''),
    ('columns[5][searchable]', 'true'),
    ('columns[5][orderable]', 'false'),
    ('columns[5][search][value]', ''),
    ('columns[5][search][regex]', 'false'),
    ('columns[6][data]', 'stake'),
    ('columns[6][name]', ''),
    ('columns[6][searchable]', 'true'),
    ('columns[6][orderable]', 'true'),
    ('columns[6][search][value]', ''),
    ('columns[6][search][regex]', 'false'),
    ('columns[7][data]', 'possible_win'),
    ('columns[7][name]', ''),
    ('columns[7][searchable]', 'true'),
    ('columns[7][orderable]', 'false'),
    ('columns[7][search][value]', ''),
    ('columns[7][search][regex]', 'false'),
    ('columns[8][data]', 'win'),
    ('columns[8][name]', ''),
    ('columns[8][searchable]', 'true'),
    ('columns[8][orderable]', 'true'),
    ('columns[8][search][value]', ''),
    ('columns[8][search][regex]', 'false'),
    ('columns[9][data]', 'updated_at'),
    ('columns[9][name]', ''),
    ('columns[9][searchable]', 'true'),
    ('columns[9][orderable]', 'true'),
    ('columns[9][search][value]', ''),
    ('columns[9][search][regex]', 'false'),
    ('columns[10][data]', 'info'),
    ('columns[10][name]', ''),
    ('columns[10][searchable]', 'true'),
    ('columns[10][orderable]', 'false'),
    ('columns[10][search][value]', ''),
    ('columns[10][search][regex]', 'false'),
    ('columns[11][data]', 'status'),
    ('columns[11][name]', ''),
    ('columns[11][searchable]', 'true'),
    ('columns[11][orderable]', 'true'),
    ('columns[11][search][value]', ''),
    ('columns[11][search][regex]', 'false'),
    ('columns[12][data]', 'placing_id'),
    ('columns[12][name]', ''),
    ('columns[12][searchable]', 'true'),
    ('columns[12][orderable]', 'false'),
    ('columns[12][search][value]', ''),
    ('columns[12][search][regex]', 'false'),
    ('columns[13][data]', 'team'),
    ('columns[13][name]', ''),
    ('columns[13][searchable]', 'true'),
    ('columns[13][orderable]', 'false'),
    ('columns[13][search][value]', ''),
    ('columns[13][search][regex]', 'false'),
    ('columns[14][data]', 'event_id'),
    ('columns[14][name]', ''),
    ('columns[14][searchable]', 'true'),
    ('columns[14][orderable]', 'false'),
    ('columns[14][search][value]', ''),
    ('columns[14][search][regex]', 'false'),
    ('columns[15][data]', 'sport_id'),
    ('columns[15][name]', ''),
    ('columns[15][searchable]', 'true'),
    ('columns[15][orderable]', 'false'),
    ('columns[15][search][value]', ''),
    ('columns[15][search][regex]', 'false'),
    ('order[0][column]', '1'),
    ('order[0][dir]', 'desc'),
    ('start', '0'),
    ('length', '10'),
    ('search[value]', ''),
    ('search[regex]', 'false'),
    ('_token', 'uL3SXQdGCXaLWwwjlcQyOKj6IODjPHdW26bYlzQW'),
    ('_', '1626424878958'),
)