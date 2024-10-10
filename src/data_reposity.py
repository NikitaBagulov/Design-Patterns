from src.core.abstract_logic import abstract_logic

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
    def keys() -> dict:
        result = {}
        methods = [method for method in dir(data_reposity) if
                callable(getattr(data_reposity, method)) and method.endswith('_key')]
        
        for method in methods:
            key_name = method.replace('_key', '')
            key_value = getattr(data_reposity, method)() 
            result[key_name] = key_value 
        
        return result
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)   