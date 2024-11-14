from src.core.abstract_logic import abstract_logic
from src.core.event_type import event_type

from src.models.nomenclature import nomenclature_model
from src.models.range import range_model
from src.models.group import group_model
from src.models.warehouse import warehouse_model
from src.models.recipe import recipe_model
from src.models.warehouse_transaction import warehouse_transaction_model
from src.models.warehouse_turnover import warehouse_turnover_model

class data_reposity(abstract_logic):
    __data = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(data_reposity, cls).__new__(cls)
        return cls.instance 

    @property
    def data(self) :
        return self.__data

    @staticmethod
    def group_key() -> str:
        return "group"

    @staticmethod
    def range_key() -> str:
        return "range"
    
    @staticmethod
    def nomenclature_key() -> str:
        return "nomenclature"
    
    @staticmethod
    def recipes_key() -> str:
        return "recipes"
    
    @staticmethod
    def warehouses_key() -> str:
        return "warehouses"
    
    @staticmethod
    def transactions_key() -> str:
        return "transactions"
    
    @staticmethod
    def turnovers_key() -> str:
        return "turnovers"
    
    @staticmethod
    def keys() -> dict:
        result = {}
        methods = [method for method in dir(data_reposity) if
                callable(getattr(data_reposity, method)) and method.endswith('_key')]
        
        for method in methods:
            key_name = method.replace('_key', '')
            key_value = getattr(data_reposity, method)() 
            result[key_name] = key_value 
        
        return result
    @staticmethod
    def create_item(key):
        model_mapping = {
            "nomenclature": nomenclature_model,
            "warehouses": warehouse_model,
            "range": range_model,
            "group": group_model,
            "recipes": recipe_model,
            "transactions": warehouse_transaction_model,
            "turnovers": warehouse_turnover_model
        }
        model_class = model_mapping.get(key)
        if model_class:
            return model_class
        else:
            raise ValueError(f"Неизвестный ключ: {key}. Невозможно создать объект.")
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)   

    
    def handle_event(self, type: event_type, params ):
        super().handle_event(type, params)