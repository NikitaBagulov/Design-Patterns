from src.core.abstract_model import abstract_model
from src.models.group import group_model
from src.models.range import range_model
from src.utils.validator import Validator

class nomenclature_model(abstract_model):
    __name: str = ""
    __full_name: str = ""
    __group: group_model = None
    __range: range_model = None


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
    def create_nomenclature_list(nomenclature_data: dict[str, range_model]) -> list['nomenclature_model']:
        nomenclature_list = []

        for name, unit in nomenclature_data.items():
            nomenclature = nomenclature_model()
            nomenclature.name = name.strip()
            nomenclature.range = unit
            nomenclature.group = group_model.default_group_source()
            nomenclature_list.append(nomenclature)

        return nomenclature_list
    
    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        Validator.validate_type(value, range_model, "range")
        self.__range = value

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

    def to_dict(self) -> dict:
        """Конвертировать объект в словарь для сериализации."""
        return {
            'name': self.unique_code,
            'full_name': self.full_name,
            'group': self.group,
            'range': self.range
        }
