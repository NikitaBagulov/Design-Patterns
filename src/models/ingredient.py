from src.abstract_model import abstract_model
from src.utils.validator import Validator

class ingredient_model(abstract_model):
    __name: str = ""
    __quantity: float = 0.0
    __unit: str = ""

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        Validator.validate_type(value, str, "name")
        Validator.validate_non_empty(value, "name")
        self.__name = value.strip()

    @property
    def quantity(self) -> float:
        return self.__quantity
    
    @quantity.setter
    def quantity(self, value: float):
        Validator.validate_positive_float(value, "quantity")
        self.__quantity = value

    @property
    def unit(self) -> str:
        return self.__unit
    
    @unit.setter
    def unit(self, value: str):
        Validator.validate_type(value, str, "unit")
        Validator.validate_non_empty(value, "unit")
        self.__unit = value.strip()

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

    def __repr__(self) -> str:
        return (
            f"<IngredientModel(name={self.__name}, "
            f"quantity={self.__quantity}, unit={self.__unit})>"
        )