from src.core.abstract_prototype import abstract_prototype
from src.core.abstract_model import abstract_model
from src.dto.filter_dto import filter_dto
from src.dto.filter_type import filter_type
from src.dto.filter_matcher import filter_matcher
from src.utils.validator import Validator
from src.utils.custom_exceptions import ArgumentException, ConversionException

class domain_prototype(abstract_prototype):

    def __init__(self, source: list) -> None:
        super().__init__(source)
        self.matcher = filter_matcher()

    def create(self, data: list, filt: filter_dto):
        self.data = self.filter_by_field(data, filt, 'name')
        self.data = self.filter_by_field(self.data, filt, 'unique_code')
        return domain_prototype(self.data)

    def filter_by_field(self, source: list, filt: filter_dto, field: str) -> list:
        """
        Универсальная функция для фильтрации по указанному полю.
        """

        Validator.validate_not_none(source, 'source')
        Validator.validate_not_none(filt, 'filt')
        Validator.validate_non_empty(field, 'field')

        # Убедимся, что фильтр имеет значение для указанного поля
        filter_value = getattr(filt, field, None)
        if filter_value is None:
            return source

        result = []
        for item in source:
            # Проверяем на соответствие полям в item и фильтре
            item_field_value = getattr(item, field, None)
            if self.match_field(item_field_value, filter_value, filt.type):
                result.append(item)
            elif self.filter_nested(item, filt, field):
                result.append(item)

        return result

    def filter_nested(self, item, filt: filter_dto, field: str) -> bool:
        """
        Рекурсивная проверка вложенных объектов на наличие поля и его фильтрацию.
        """

        Validator.validate_not_none(item, 'item')
        Validator.validate_not_none(filt, 'filt')
        Validator.validate_non_empty(field, 'field')

        for attr_name in dir(item):
            attr_value = getattr(item, attr_name)
            if isinstance(attr_value, abstract_model):
                nested_field_value = getattr(attr_value, field, None)
                if self.match_field(nested_field_value, getattr(filt, field), filt.type):
                    return True
            elif isinstance(attr_value, list):
                for nested_item in attr_value:
                    if isinstance(nested_item, abstract_model):
                        nested_field_value = getattr(nested_item, field, None)
                        if self.match_field(nested_field_value, getattr(filt, field), filt.type):
                            return True
        return False

    def match_field(self, field_value: str, filter_value: str, filter_type: filter_type) -> bool:
        """
        Универсальная функция для сравнения полей по типу фильтрации.
        """
        if not field_value or not filter_value:
            return False

        try:
            return self.matcher.match_field(field_value, filter_value, filter_type)
        except ArgumentException as ae:
            print(f"Ошибка аргумента: {ae}")
            return False
        except ConversionException as ce:
            print(f"Ошибка преобразования: {ce}")
            return False
        except Exception as ex:
            print(f"Ошибка: {ex}")
            return False
