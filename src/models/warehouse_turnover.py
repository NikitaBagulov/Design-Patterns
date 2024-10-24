from src.core.abstract_model import abstract_model
from src.utils.validator import Validator
from src.models.warehouse import warehouse_model
from src.models.nomenclature import nomenclature_model
from src.models.range import range_model

class warehouse_turnover_model(abstract_model):
    __warehouse: warehouse_model
    __turnover: float = 0.0
    __nomenclature: nomenclature_model
    __range: range_model

    @property
    def warehouse(self) -> warehouse_model:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: warehouse_model):
        Validator.validate_not_none(value, "warehouse")
        Validator.validate_type(value, warehouse_model, "warehouse")
        self.__warehouse = value

    @property
    def turnover(self) -> float:
        return self.__turnover

    @turnover.setter
    def turnover(self, value: float):
        self.__turnover = value

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        Validator.validate_not_none(value, "nomenclature")
        Validator.validate_type(value, nomenclature_model, "nomenclature")
        self.__nomenclature = value

    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        Validator.validate_not_none(value, "range")
        Validator.validate_type(value, range_model, "range")
        self.__range = value

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

    def _deserialize_additional_fields(self):
        pass

    @staticmethod
    def create(warehouse: warehouse_model, nomenclature: nomenclature_model, range: range_model, turnover: float = 0.0):
        """
        Статический фабричный метод для создания экземпляра warehouse_turnover_model.
        """
        Validator.validate_not_none(warehouse, "warehouse")
        Validator.validate_type(warehouse, warehouse_model, "warehouse")
        
        Validator.validate_not_none(nomenclature, "nomenclature")
        Validator.validate_type(nomenclature, nomenclature_model, "nomenclature")
        
        Validator.validate_not_none(range, "range")
        Validator.validate_type(range, range_model, "range")

        instance = warehouse_turnover_model()
        instance.warehouse = warehouse
        instance.nomenclature = nomenclature
        instance.range = range
        instance.turnover = turnover
        return instance
