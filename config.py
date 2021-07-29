import os
from pathlib import Path

BASE_PATH = Path(__file__).resolve(strict=True).parent

if not os.path.exists(BASE_PATH / 'screenshots'):
    os.mkdir(BASE_PATH / 'screenshots')

DEBUG = True

EXECUTABLE_PATH = BASE_PATH / 'chromedriver'  # chromedriver path

