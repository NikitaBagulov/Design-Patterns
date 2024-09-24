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
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)   