from enum import Enum


class SiteUrlEnum(str, Enum):

    DEV = "https://dev.nuxbet.com/"
    # PROD = "https://nuxbet.com/"
    SFRONT1 = "https://sfront1.nuxbet.com/"
    SFRONT3 = "https://sfront3.nuxbet.com/"


    def __str__(self):
        return str(self.value)


class CredentialEnum(str, Enum):

    REFERAL_CODE = "QwERty123!@#"
    PASSWORD = "secretZ1"
    DEFAULT_MAIL = "nuxbetchk@gmail.com"
    AUTHORISATION_SHORT_NAME = "autotestuser1672"
    AUTHORISATION_NAME = "autotestuser1672@mail.com"
    PASSWD = "secretZ1"
    ADMIN_PASSWORD = "secretZ13"
