from src.models.settings import settings
from src.abstract_model import abstract_model
from src.custom_exceptions import LengthException, ArgumentException

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
        try:
            if not isinstance(value, str) or len(value) != 12 or not value.isdigit():
                raise LengthException("ИНН", 12)
            self.__inn = value
        except LengthException as e:
            raise ArgumentException("inn", str(e)) from e

    @property
    def bik(self) -> str:
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        try:
            if not isinstance(value, str) or len(value) != 9 or not value.isdigit():
                raise LengthException("БИК", 9)
            self.__bik = value
        except LengthException as e:
            raise ArgumentException("bik", str(e)) from e

    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, value: str):
        try:
            if not isinstance(value, str) or len(value) != 11 or not value.isdigit():
                raise LengthException("Счет", 11)
            self.__account = value
        except LengthException as e:
            raise ArgumentException("account", str(e)) from e

    @property
    def ownership_type(self) -> str:
        return self.__ownership_type

    @ownership_type.setter
    def ownership_type(self, value: str):
        try:
            if not isinstance(value, str) or len(value) != 5:
                raise LengthException("Вид собственности", 5)
            self.__ownership_type = value
        except LengthException as e:
            raise ArgumentException("ownership_type", str(e)) from e

    def load_from_settings(self, settings: settings):
        try:
            self.inn = settings.inn
            self.bik = settings.bik
            self.account = settings.account
            self.ownership_type = settings.ownership_type
        except ArgumentException as e:
            print(f"Ошибка загрузки данных из настроек: {e}")

    def set_compare_mode(self, other_object) -> bool:
        if other_object is None:
            return False
        if not isinstance(other_object, company_model):
            return False
        return (self.inn == other_object.inn and
                self.bik == other_object.bik and
                self.account == other_object.account and
                self.ownership_type == other_object.ownership_type)
