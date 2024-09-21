from src.abstract_model import abstract_model
from src.utils.validator import Validator

class range_model(abstract_model):
    __name: str = ""
    __base_unit: 'range_model' = None
    __conversion_factor: int = 1  

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        Validator.validate_type(value, str, "name")
        Validator.validate_non_empty(value, "name")
        self.__name = value.strip()

    @property
    def base_unit(self) -> 'range_model':
        return self.__base_unit

    def set_base_unit(self, base_unit: 'range_model', conversion_factor: int):
        if base_unit is not None:
            Validator.validate_type(base_unit, range_model, "base_unit") 
        Validator.validate_positive_integer(conversion_factor, "conversion_factor")
        self.__base_unit = base_unit
        self.__conversion_factor = conversion_factor

    @property
    def conversion_factor(self) -> int:
        return self.__conversion_factor

    @staticmethod
    def default_unit_kg():
        item = range_model()
        item.name = "Килограмм"
        item.set_base_unit(None, 1)
        return item

    @staticmethod
    def default_unit_piece():
        item = range_model()
        item.name = "Штука"
        item.set_base_unit(None, 1)
        return item

    @staticmethod
    def default_unit_gram():
        item = range_model()
        item.name = "Грамм"
        kg_unit = range_model.default_unit_kg()
        item.set_base_unit(kg_unit, 1000)
        return item

    def set_compare_mode(self, other_object) -> bool:
        if other_object is None:
            return False
        if not isinstance(other_object, range_model):
            return False
        return self.__name == other_object.__name
                
