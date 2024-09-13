from src.abstract_model import abstract_model
from src.custom_exceptions import LengthException, ArgumentException

class nomenclature_group_model(abstract_model):
    __name: str = ""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        try:
            if not value or len(value) > 50:
                raise LengthException("name", 50)
            self.__name = value.strip()
        except LengthException as e:
            raise ArgumentException("name", str(e)) from e

    def set_compare_mode(self, other_object) -> bool:
        if other_object is None:
            return False
        if not isinstance(other_object, nomenclature_group_model):
            return False
        return self.__name == other_object.__name
