from src.core.abstract_model import abstract_model
from src.models.group import group_model
from src.models.range import range_model
from src.utils.validator import Validator

class nomenclature_model(abstract_model):
    __name: str = ""
    __full_name: str = ""
    __group: group_model = group_model.default_group_source()
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
        if other_object is None:
            return False
        if not isinstance(other_object, nomenclature_model):
            return False

        return self.unique_code == other_object.unique_code


    def __str__(self) -> str:
        return (
            f"<NomenclatureModel(name='{self.__name}', "
            f"full_name='{self.__full_name}', "
            f"range={self.__range}, "
            f"group={self.__group}),"
            f"unique_code={self.unique_code})>"
        )

    def _deserialize_additional_fields(self, data: dict):
        """
        Десериализация дополнительных полей для nomenclature_model.
        """
        if 'full_name' in data:
            self.full_name = data['full_name']

        if 'group' in data and isinstance(data['group'], dict):
            group_data = data['group']
            group_instance = group_model()  
            group_instance.deserialize(group_data)
            self.group = group_instance 

        if 'range' in data and isinstance(data['range'], dict):
            range_data = data['range']
            range_instance = range_model()
            range_instance.deserialize(range_data)
            self.range = range_instance
