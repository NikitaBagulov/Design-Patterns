from src.dto.filter_type import filter_type
from src.utils.validator import Validator
from src.utils.custom_exceptions import ArgumentException
from src.core.abstract_logic import abstract_logic

class filter_dto(abstract_logic):
    def __init__(self, name: str = "", unique_code: str = "", type: filter_type = filter_type.EQUALS):
        self.__name: str = name
        self.__unique_code: str = unique_code
        self.__type: filter_type = type

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        try:
            Validator.validate_non_empty(value, "name")
            Validator.validate_length(value, 50, "name")
            self.__name = value
        except ArgumentException as ex:
            self.set_exception(ex)

    @property
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, value: str):
        try:
            Validator.validate_non_empty(value, "unique_code")
            self.__unique_code = value
        except ArgumentException as ex:
            self.set_exception(ex)

    @property
    def type(self) -> filter_type:
        return self.__type
    
    @type.setter
    def type(self, value: filter_type):
        try:
            Validator.validate_enum_value(value, filter_type, "type")
            self.__type = value
        except ArgumentException as ex:
            self.set_exception(ex)

    @staticmethod
    def from_dict(data):
        try:
            name = data.get('name', "")
            unique_code = data.get('unique_code', "")
            type_value = int(data.get('type', filter_type.EQUALS.value))
            
            type_enum = filter_type(type_value)
            
            Validator.validate_length(name, 50, "name")
            Validator.validate_length(unique_code, 20, "unique_code")
            Validator.validate_enum_value(type_enum, filter_type, "type")
        
            return filter_dto(
                name=name,
                unique_code=unique_code,
                type=type_enum
            )
        except ArgumentException as ex:
            filter_dto().set_exception(ex)
        except Exception as ex:
            filter_dto().set_exception(ex)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
