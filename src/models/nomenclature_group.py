from src.abstract_model import abstract_model
from src.utils.validator import Validator

class nomenclature_group_model(abstract_model):
    __name: str = ""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        Validator.validate_length(value, 50, "name")
        self.__name = value.strip()

    def set_compare_mode(self, other_object) -> bool:
        if other_object is None:
            return False
        if not isinstance(other_object, nomenclature_group_model):
            return False
        return self.__name == other_object.__name
