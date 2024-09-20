from src.utils.custom_exceptions import ArgumentException, LengthException, DigitsException, ConversionException
# from src.models.range import range_model

class Validator:
    @staticmethod
    def validate_length(value: str, max_length: int, field_name: str):
        """Проверяет длину строки и создает исключение, если длина превышает допустимый лимит."""
        if len(value) > max_length:
            raise LengthException(field_name, max_length)

    @staticmethod
    def validate_digits(value: str, length: int, field_name: str):
        """Проверяет, что строка состоит из цифр определенной длины и создает исключение, если это не так."""
        if not isinstance(value, str) or len(value) != length or not value.isdigit():
            raise DigitsException(field_name, length)
    
    @staticmethod
    def validate_positive(value: int, field_name: str):
        """Проверяет, что значение положительное и создает исключение, если это не так."""
        if value <= 0:
            raise ArgumentException(field_name, "Значение должно быть положительным")

    @staticmethod
    def validate_not_none(value, field_name: str):
        """Проверяет, что значение не равно None и создает исключение, если это не так."""
        if value is None:
            raise ArgumentException(field_name, "Не может быть None")

    @staticmethod
    def validate_non_empty(value: str, argument_name: str):
        """Проверяет, что строка не является пустой."""
        if not value.strip():
            raise ArgumentException(argument_name, "Значение аргумента не должно быть пустым")

    @staticmethod
    def validate_positive_integer(value: int, argument_name: str):
        """Проверяет, что значение является положительным целым числом."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"Значение аргумента '{argument_name}' должно быть положительным целым числом.")
    
    @staticmethod
    def validate_positive_float(value: float, argument_name: str) -> None:
        if not isinstance(value, (float, int)):
            raise ValueError(f"Значение аргумента '{argument_name}' должно быть числом с плавающей запятой.")
        if value <= 0:
            raise ValueError(f"Значение аргумента '{argument_name}' должно быть положительным числом.")

    @staticmethod
    def validate_type(value, expected_type, field_name: str):
        """Проверяет тип значения и создает исключение, если тип не совпадает с ожидаемым."""
        if not isinstance(value, expected_type):
            raise ArgumentException(field_name, f"Должно быть типа {expected_type.__name__}")

    @staticmethod
    def validate_value(value, expected_value, field_name: str):
        """Проверяет значение на соответствие ожидаемому и создает исключение, если это не так."""
        if value != expected_value:
            raise ArgumentException(field_name, f"Должно быть {expected_value}")

