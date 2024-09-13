from src.abstract_model import abstract_model
from src.models.nomenclature_group import nomenclature_group_model
from src.models.range import range_model
from src.custom_exceptions import LengthException, ArgumentException

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
        try:
            if not value or len(value) > 50:
                raise LengthException("name", 50)
            self.__name = value.strip()
        except LengthException as e:
            raise ArgumentException("name", str(e)) from e

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str):
        try:
            if len(value) > 255:
                raise LengthException("full_name", 255)
            self.__full_name = value.strip()
        except LengthException as e:
            raise ArgumentException("full_name", str(e)) from e

    @property
    def group(self) -> nomenclature_group_model:
        return self.__group

    @group.setter
    def group(self, value: nomenclature_group_model):
        if not isinstance(value, nomenclature_group_model):
            raise ArgumentException("group", "Не является группой номенклатуры!")
        self.__group = value

    @property
    def unit(self) -> range_model:
        return self.__unit

    @unit.setter
    def unit(self, value: range_model):
        if not isinstance(value, range_model):
            raise ArgumentException("unit", "Не является базовой единицей!")
        self.__unit = value

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object) 
