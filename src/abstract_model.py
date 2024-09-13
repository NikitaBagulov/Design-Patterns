from abc import ABC, abstractmethod
import uuid
from src.custom_exceptions import LengthException, ArgumentException

class abstract_model(ABC):
    __unique_code: str = uuid.uuid4()
    __name: str = ""

    @property
    def unique_code(self) -> str:
        return self.__unique_code

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        try:
            if not isinstance(value, str) or len(value) > 50:
                raise LengthException("name", 50)
            self.__name = value.strip()
        except LengthException as e:
            raise ArgumentException("name", str(e)) from e

    @abstractmethod
    def set_compare_mode(self, other_object) -> bool:
        if other_object is None:
            return False
        if not isinstance(other_object, abstract_model):
            return False

        return self.__unique_code == other_object.unique_code

    def __eq__(self, value: object) -> bool:
        return self.set_compare_mode(value)
