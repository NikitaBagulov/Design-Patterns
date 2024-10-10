from abc import ABC, abstractmethod
from src.core.abstract_model import abstract_model
from src.utils.validator import Validator


class abstract_prototype(ABC):
    __data = []

    def __init__(self, source:list) -> None:
        super().__init__()
        # validator.validate(source, list)
        self.__data = source

    @abstractmethod
    def create(self, data:list, filter):
        # validator.validate(data, list)
        pass

    @property
    def data(self) -> list:
        return self.__data    
    
    @data.setter
    def data(self, value:list):
        self.__data = value