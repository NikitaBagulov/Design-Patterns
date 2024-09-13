from src.abstract_model import abstract_model
from src.models.settings import settings
from src.utils.validator import Validator

class company_model(abstract_model):
    __inn: str = ""
    __bik: str = ""
    __account: str = ""
    __ownership_type: str = ""

    @property
    def inn(self) -> str:
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        Validator.validate_digits(value, 12, "ИНН")
        self.__inn = value

    @property
    def bik(self) -> str:
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        Validator.validate_digits(value, 9, "БИК")
        self.__bik = value

    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, value: str):
        Validator.validate_digits(value, 11, "Счет")
        self.__account = value

    @property
    def ownership_type(self) -> str:
        return self.__ownership_type

    @ownership_type.setter
    def ownership_type(self, value: str):
        Validator.validate_length(value, 5, "Форма собственности")
        self.__ownership_type = value

    def load_from_settings(self, settings: settings):
        """Загружает данные компании из объекта настроек."""
        self.inn = settings.inn
        self.account = settings.account
        self.bik = settings.bik
        self.ownership_type = settings.ownership_type

    def set_compare_mode(self, other_object) -> bool:
        if other_object is None:
            return False
        if not isinstance(other_object, company_model):
            return False
        return (self.inn == other_object.inn and
                self.bik == other_object.bik and
                self.account == other_object.account and
                self.ownership_type == other_object.ownership_type)
