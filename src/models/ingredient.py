from src.core.abstract_model import abstract_model
from src.models.nomenclature import nomenclature_model
from src.models.range import range_model
from src.utils.validator import Validator

class ingredient_model(abstract_model):
    __nomenclature: nomenclature_model = None
    __quantity: float = 0.0

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        Validator.validate_type(value, nomenclature_model, "nomenclature")
        self.__nomenclature = value

    @property
    def quantity(self) -> float:
        self.__quantity = float(self.__quantity)
        Validator.validate_positive_float(self.__quantity, "quantity")
        return self.__quantity
    
    @quantity.setter
    def quantity(self, value: float):
        self.__quantity = value

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)
