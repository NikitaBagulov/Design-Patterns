from src.core.abstract_model import abstract_model
from src.utils.validator import Validator

class warehouse_model(abstract_model):
    __name: str = ""
    __address: str = ""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        Validator.validate_length(value, 50, "name")
        self.__name = value.strip()

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str):
        Validator.validate_length(value, 100, "address")
        self.__address = value.strip()

    def set_compare_mode(self, other_object) -> bool:
        if other_object is None:
            return False
        if not isinstance(other_object, warehouse_model):
            return False
        return (self.__name == other_object.__name and
                self.__address == other_object.__address)
    
    def _deserialize_additional_fields(self):
        pass
