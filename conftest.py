import pytest
from enums import SiteUrlEnum, CredentialEnum
from browser_creator import Driver


@pytest.fixture(scope="session")
def browser():
    driver = Driver()
    yield driver


@pytest.fixture(scope="session")
def urls():
    yield SiteUrlEnum.to_dict()


@pytest.fixture(scope="session")
def creds():
    yield CredentialEnum
