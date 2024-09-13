from src.abstract_model import abstract_model
from src.models.nomenclature_group import nomenclature_group_model
from src.models.range import range_model
from src.utils.validator import Validator

class nomenclature_model(abstract_model):
    __name: str = ""
    __full_name: str = ""
    __group: nomenclature_group_model = None
    __unit: range_model = None

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        Validator.validate_length(value, 50, "name")
        self.__name = value.strip()

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str):
        Validator.validate_length(value, 255, "full_name") 
        self.__full_name = value.strip()

    @property
    def group(self) -> nomenclature_group_model:
        return self.__group

    @group.setter
    def group(self, value: nomenclature_group_model):
        Validator.validate_type(value, nomenclature_group_model, "group") 
        self.__group = value

    @property
    def unit(self) -> range_model:
        return self.__unit

    @unit.setter
    def unit(self, value: range_model):
        Validator.validate_type(value, range_model, "unit") 
        self.__unit = value

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)
