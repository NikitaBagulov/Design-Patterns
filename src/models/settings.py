from src.custom_exceptions import LengthException, DigitsException

class settings:
    def __init__(self):
        self.__organization_name = ""
        self.__inn = ""
        self.__account = ""
        self.__corr_account = ""
        self.__bik = ""
        self.__ownership_type = ""

    @property
    def organization_name(self):
        return self.__organization_name
    
    @organization_name.setter
    def organization_name(self, value: str):
        if not isinstance(value, str) or len(value) > 255:
            raise LengthException("organization_name", 255)
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn
    
    @inn.setter
    def inn(self, value: str):
        if not value.isdigit() or len(value) != 12:
            raise DigitsException("ИНН", 12)
        self.__inn = value

    @property
    def account(self):
        return self.__account
    
    @account.setter
    def account(self, value: str):
        if not value.isdigit() or len(value) != 11:
            raise DigitsException("Счет", 11)
        self.__account = value

    @property
    def corr_account(self):
        return self.__corr_account
    
    @corr_account.setter
    def corr_account(self, value: str):
        if not value.isdigit() or len(value) != 11:
            raise DigitsException("Корреспондентский счет", 11)
        self.__corr_account = value

    @property
    def bik(self):
        return self.__bik
    
    @bik.setter
    def bik(self, value: str):
        if not value.isdigit() or len(value) != 9:
            raise DigitsException("БИК", 9)
        self.__bik = value

    @property
    def ownership_type(self):
        return self.__ownership_type
    
    @ownership_type.setter
    def ownership_type(self, value: str):
        if not isinstance(value, str) or len(value) != 5:
            raise LengthException("Форма собственности", 5)
        self.__ownership_type = value
