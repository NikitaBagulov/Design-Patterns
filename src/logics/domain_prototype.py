from src.core.abstract_prototype import abstract_prototype
from src.core.abstract_model import abstract_model
from src.dto.filter import filter
from src.dto.filter_type import filter_type

class domain_prototype(abstract_prototype):

    def __init__(self, source: list) -> None:
        super().__init__(source)

    def create(self, data: list, filter_dto: filter):
        self.data = self.filter_by_field(data, filter_dto, 'name')
        self.data = self.filter_by_field(self.data, filter_dto, 'unique_code')
        return domain_prototype(self.data)

    def filter_by_field(self, source: list, filter_dto: filter, field: str) -> list:
        """
        Универсальная функция для фильтрации по указанному полю.
        """
        if not getattr(filter_dto, field, None):
            return source

        result = []
        for item in source:
            if self.match_field(getattr(item, field, None), getattr(filter_dto, field), filter_dto.type):
                result.append(item)
            elif self.filter_nested(item, filter_dto, field):
                result.append(item)

        return result

    def filter_nested(self, item, filter_dto: filter, field: str) -> bool:
        """
        Рекурсивная проверка вложенных объектов на наличие поля и его фильтрацию.
        """
        for attr_name in dir(item):
            attr_value = getattr(item, attr_name)
            if isinstance(attr_value, abstract_model) and self.match_field(getattr(attr_value, field, None), getattr(filter_dto, field), filter_dto.type):
                return True
            elif isinstance(attr_value, list):
                for nested_item in attr_value:
                    if isinstance(nested_item, abstract_model) and self.match_field(getattr(nested_item, field, None), getattr(filter_dto, field), filter_dto.type):
                        return True
        return False

    def match_field(self, field_value: str, filter_value: str, filter_type: filter_type) -> bool:
        """
        Универсальная функция для сравнения полей по типу фильтрации.
        """
        if not field_value or not filter_value:
            return False

        if filter_type == filter_type.EQUALS:
            return field_value == filter_value
        elif filter_type == filter_type.LIKE:
            return filter_value in field_value
        return False