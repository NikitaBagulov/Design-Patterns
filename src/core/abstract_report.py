from abc import ABC, abstractmethod
from src.core.format_reporting import format_reporting
from src.utils.validator import Validator

class abstract_report(ABC):
    __format: format_reporting = format_reporting.CSV
    __result:str = ""


    @abstractmethod
    def create(self, data: list):
        pass

    @property
    def format(self) -> format_reporting:
        return self.__format
    
    @property
    def result(self) -> str:
        return self.__result
    
    @result.setter
    def result(self, value:str):
        Validator.validate_type(value, str, "result")
        self.__result = value
