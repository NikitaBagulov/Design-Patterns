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
    def create(data):
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

class warehouse_nomenclature_filter_dto(abstract_logic):
    def __init__(self, warehouse: filter_dto = None, nomenclature: filter_dto = None, period: dict = None):
        self.__warehouse: filter_dto = warehouse
        self.__nomenclature: filter_dto = nomenclature
        self.__period: dict = period

    @property
    def warehouse(self) -> filter_dto:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: filter_dto):
        self.__warehouse = value

    @property
    def nomenclature(self) -> filter_dto:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: filter_dto):
        self.__nomenclature = value

    @property
    def period(self) -> dict:
        return self.__period

    @period.setter
    def period(self, value: dict):
        try:
            start = value.get('start')
            end = value.get('end')
            if start and end:
                Validator.validate_non_empty(start, "period start")
                Validator.validate_non_empty(end, "period end")
            self.__period = value
        except ArgumentException as ex:
            self.set_exception(ex)

    @staticmethod
    def create(data):
        try:
            warehouse_data = data.get('warehouse', {})
            nomenclature_data = data.get('nomenclature', {})
            start_period = data.get('start_period', None)
            end_period = data.get('end_period', None)

            warehouse = filter_dto.create(warehouse_data)
            nomenclature = filter_dto.create(nomenclature_data)

            period_data = {}
            if start_period and end_period:
                period_data = {
                    'start': start_period,
                    'end': end_period
                }

            return warehouse_nomenclature_filter_dto(
                warehouse=warehouse,
                nomenclature=nomenclature,
                period=period_data
            )
        except ArgumentException as ex:
            warehouse_nomenclature_filter_dto().set_exception(ex)
        except Exception as ex:
            warehouse_nomenclature_filter_dto().set_exception(ex)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
