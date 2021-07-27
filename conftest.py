import pytest
from browser_creator import Driver


@pytest.fixture(scope="session")
def browser():
    driver = Driver()
    yield driver
    driver.quit()
