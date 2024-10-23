from src.core.abstract_model import abstract_model
from src.utils.validator import Validator
from src.models.nomenclature import nomenclature_model
from src.models.range import range_model
from src.models.warehouse import warehouse_model
from datetime import datetime

class warehouse_transaction_model(abstract_model):
    __warehouse: warehouse_model
    __nomenclature: nomenclature_model
    __quantity: float = 0.0
    __range: range_model
    __period: datetime
    __is_incoming: bool = True

    @property
    def warehouse(self) -> warehouse_model:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: warehouse_model):
        Validator.validate_not_none(value, "warehouse")
        Validator.validate_type(value, warehouse_model, "warehouse")
        self.__warehouse = value

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        Validator.validate_not_none(value, "nomenclature")
        Validator.validate_type(value, nomenclature_model, "nomenclature")
        self.__nomenclature = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        Validator.validate_positive_float(value, "quantity")
        self.__quantity = value

    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        Validator.validate_not_none(value, "range")
        Validator.validate_type(value, range_model, "range")
        self.__range = value

    @property
    def period(self) -> datetime:
        return self.__period

    @period.setter
    def period(self, value: datetime):
        Validator.validate_not_none(value, "period")
        Validator.validate_type(value, datetime, "period")
        self.__period = value

    @property
    def is_incoming(self) -> bool:
        return self.__is_incoming

    @is_incoming.setter
    def is_incoming(self, value: bool):
        Validator.validate_type(value, bool, "is_incoming")
        self.__is_incoming = value

    @staticmethod
    def create(warehouse: warehouse_model, nomenclature: nomenclature_model, quantity: float,
               range: range_model, period: datetime, is_incoming: bool = True) -> 'warehouse_transaction_model':
        transaction = warehouse_transaction_model()
        transaction.warehouse = warehouse
        transaction.nomenclature = nomenclature
        transaction.quantity = quantity
        transaction.range = range
        transaction.period = period
        transaction.is_incoming = is_incoming
        return transaction

    def set_compare_mode(self, other_object) -> bool:
        super().set_compare_mode(other_object)

    def _deserialize_additional_fields(self):
        pass
