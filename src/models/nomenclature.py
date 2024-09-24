from src.core.abstract_model import abstract_model
from src.models.group import group_model
from src.models.range import range_model
from src.utils.validator import Validator

class nomenclature_model(abstract_model):
    __name: str = ""
    __full_name: str = ""
    __group: group_model = None


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
    def group(self) -> group_model:
        return self.__group

    @group.setter
    def group(self, value: group_model):
        Validator.validate_type(value, group_model, "group") 
        self.__group = value

    @staticmethod
    def create_nomenclature_list(names: list[str]) -> list['nomenclature_model']:
        nomenclature_list = []

        for name in names:
            nomenclature = nomenclature_model()
            nomenclature.name = name.strip()
            nomenclature_list.append(nomenclature)

        return nomenclature_list

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)
