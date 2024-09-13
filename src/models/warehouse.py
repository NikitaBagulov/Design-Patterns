from src.abstract_model import abstract_model
from src.custom_exceptions import LengthException, ArgumentException

class warehouse_model(abstract_model):
    __name: str = ""
    __address: str = ""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        try:
            if len(value) > 50:
                raise LengthException("name", 50)
            self.__name = value.strip()
        except LengthException as e:
            raise ArgumentException("name", str(e)) from e

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str):
        try:
            if len(value) > 100:
                raise LengthException("address", 100)
            self.__address = value.strip()
        except LengthException as e:
            raise ArgumentException("address", str(e)) from e

    def set_compare_mode(self, other_object) -> bool:
        if other_object is None:
            return False
        if not isinstance(other_object, warehouse_model):
            return False
        return (self.__name == other_object.__name and
                self.__address == other_object.__address)
