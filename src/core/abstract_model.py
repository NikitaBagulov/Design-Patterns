from abc import ABC, abstractmethod
import uuid
from src.utils.custom_exceptions import LengthException, ArgumentException

class abstract_model(ABC):
    def __init__(self):
        self.__unique_code: str = uuid.uuid4().hex
        self.__name: str = ""

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
        pass

    def __eq__(self, value: object) -> bool:
        return self.set_compare_mode(value)
    
    def __str__(self) -> str:
        return self.__unique_code
    
    def deserialize(self, data: dict):
        """
        Десериализует объект из словаря данных.
        """
        if not isinstance(data, dict):
            raise ArgumentException("data", "Ожидается словарь для десериализации")

        if "unique_code" in data and data["unique_code"]:
            self.__unique_code = data["unique_code"]

        if "name" in data:
            self.name = data["name"]

        self._deserialize_additional_fields(data)

    @abstractmethod
    def _deserialize_additional_fields(self, data: dict):
        """
        Абстрактный метод для десериализации дополнительных полей.
        """
        pass

