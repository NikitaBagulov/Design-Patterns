from src.dto.filter_type import filter_type

class filter_dto:
    def __init__(self, name: str = "", unique_code: str = "", type: filter_type = filter_type.EQUALS):
        self.__name:str = name
        self.__unique_code:str = unique_code
        self.__type: filter_type = type

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value:str):
        self.__name = value

    @property
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, value: str):
        self.__unique_code = value  

    @property
    def type(self) -> filter_type:
        return self.__type
    
    @type.setter
    def type(self, value: filter_type):
        self.__type = value

    @staticmethod
    def from_dict(data):
        type_str = data.get('type', 'EQUALS').upper()
        type_enum = getattr(filter_type, type_str, filter_type.EQUALS)
        print(type_enum)

        return filter_dto(
            name=data.get('name'),
            unique_code=data.get('unique_code'),
            type=type_enum
        )