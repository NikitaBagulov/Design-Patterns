class BaseCustomException(Exception):
    """Базовое исключение для всех ошибок."""
    pass

class ArgumentException(BaseCustomException):
    """Исключение для ошибок передачи аргументов."""
    def __init__(self, argument_name: str, message: str = "Некорректный аргумент"):
        self.argument_name = argument_name
        self.message = f"{message}: {argument_name}"
        super().__init__(self.message)

class LengthException(ArgumentException):
    """Исключение для ошибок, связанных с длиной строки."""
    def __init__(self, argument_name: str, max_length: int):
        self.message = f"Длина '{argument_name}' превышает допустимый лимит в {max_length} символов"
        super().__init__(argument_name, self.message)

class DigitsException(ArgumentException):
    """Исключение для ошибок, связанных с длиной строки и цифрами."""
    def __init__(self, argument_name: str, length: int):
        self.message = f"'{argument_name}' должен содержать {length} цифр"
        super().__init__(argument_name, self.message)

class ConversionException(BaseCustomException):
    """Исключение для ошибок преобразования единиц измерения."""
    def __init__(self, message: str = "Некорректное преобразование"):
        super().__init__(message)

class NotFoundException(BaseCustomException):
    """Исключение для ошибок, связанных с отсутствием файла или данных."""
    def __init__(self, item: str = "Файл или элемент"):
        super().__init__(f"{item} не найден(а)")
