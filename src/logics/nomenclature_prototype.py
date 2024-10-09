from src.core.abstract_prototype import abstract_prototype
from src.dto.filter import filter


class nomenclature_prototype(abstract_prototype):

    def __init__(self, source: list) -> None:
        super().__init__(source)

    def create(self, data: list, filterDto: filter):
        super().create(data, filterDto)
        self.data =  self.filter_name(data, filterDto);
        self.data =  self.filter_id(self.data, filterDto);
        instance = nomenclature_prototype(self.data )
        return instance


    def filter_name(self, source:list, filterDto: filter) -> list:
        if filterDto.name == "" or filterDto.name == None:
            return source
        
        result = []
        for item in source:
            if item.name == filterDto.name:
                result.append(item)

        return result        

    def filter_id(self, source:list, filterDto: filter) -> list:
        if filterDto.id == "" or filterDto.id == None:
            return source
        
        result = []
        for item in source:
            if item.unique_code == filterDto.id:
                result.append(item)

        return result      