import os
from pathlib import Path

BASE_PATH = Path(__file__).resolve(strict=True).parent
SCREENSHOT_PATH = BASE_PATH / "screenshots"

if not os.path.exists(SCREENSHOT_PATH):
    os.mkdir(SCREENSHOT_PATH)

DEBUG = True

EXECUTABLE_PATH = BASE_PATH / 'chromedriver'  # chromedriver path
