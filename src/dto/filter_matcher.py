from src.dto.filter_type import filter_type
from src.utils.validator import Validator
from src.utils.custom_exceptions import ArgumentException, ConversionException

class filter_matcher:
    def __init__(self):
        self.matching_functions = {ft: getattr(self, ft.name.lower()) for ft in filter_type}

    def match_field(self, field_value: str, filter_value: str, filter_type: filter_type) -> bool:
        """
        Универсальная функция для сравнения полей по типу фильтрации.
        """
        if filter_type in self.matching_functions:
            return self.matching_functions[filter_type](field_value, filter_value)
        return False

    def equals(self, field_value: str, filter_value: str) -> bool:
        if Validator.validate_non_empty(field_value, "field_value") or Validator.validate_non_empty(filter_value, "filter_value"):
            raise ArgumentException('field_value или filter_value', 'Параметры не могут быть пустыми')
        return field_value == filter_value

    def like(self, field_value: str, filter_value: str) -> bool:
        if Validator.validate_non_empty(field_value, "field_value") or Validator.validate_non_empty(filter_value, "filter_value"):
            raise ArgumentException('field_value или filter_value', 'Параметры не могут быть пустыми')
        return filter_value in field_value

    def greater_than(self, field_value: str, filter_value: str) -> bool:
        try:
            if Validator.validate_non_empty(field_value, "field_value") or Validator.validate_non_empty(filter_value, "filter_value"):
                raise ArgumentException('field_value или filter_value', 'Параметры не могут быть пустыми')
            return float(field_value) > float(filter_value)
        except ValueError:
            raise ConversionException("Ошибка преобразования в float для greater_than")

    def less_than(self, field_value: str, filter_value: str) -> bool:
        try:
            if Validator.validate_non_empty(field_value) or Validator.validate_non_empty(filter_value):
                raise ArgumentException('field_value или filter_value', 'Параметры не могут быть пустыми')
            return float(field_value) < float(filter_value)
        except ValueError:
            raise ConversionException("Ошибка преобразования в float для less_than")

    def in_range(self, field_value: str, filter_values: str) -> bool:
        try:
            if Validator.is_empty(field_value) or Validator.is_empty(filter_values):
                raise ArgumentException('field_value или filter_values', 'Параметры не могут быть пустыми')
            min_val, max_val = map(float, filter_values.split(","))
            return min_val <= float(field_value) <= max_val
        except (ValueError, TypeError):
            raise ConversionException("Некорректное преобразование диапазона в in_range")
