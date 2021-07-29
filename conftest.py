import pytest
from helpers.enums import CredentialEnum
from helpers.browser_creator import Driver


@pytest.fixture(scope="session")
def browser():
    driver = Driver()
    yield driver


@pytest.fixture(scope="session")
def creds():
    yield CredentialEnum
