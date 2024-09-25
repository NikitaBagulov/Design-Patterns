from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.utils.validator import Validator

class csv_report(abstract_report):

    def __init__(self) -> None:
       super().__init__()
       self.__format = format_reporting.CSV

    def create(self, data: list):
        Validator.validate_type(data, list, "data")
        
        first_model = data[0]
        print(first_model)
        fields = self.get_fields(first_model)

        # Формирование заголовков CSV
        for field in fields:
            self.result += f"{str(field)};"
        self.result += "\n"

        # Формирование данных
        for row in data:
            for field in fields:
                value = getattr(row, field)
                self.result += f"{self.serialize_value(value)};"
            self.result += "\n"

    def get_fields(self, obj):
        """Получаем список полей модели, исключая приватные и callable-атрибуты"""
        return list(filter(lambda x: not x.startswith("_") and not callable(getattr(obj.__class__, x)), dir(obj)))

    def serialize_value(self, value):
        """Рекурсивная сериализация значений, включая вложенные объекты"""
        if isinstance(value, list):
            return "[" + ", ".join([self.serialize_value(v) for v in value]) + "]"
        elif hasattr(value, "__dict__"):  # Объект модели
            fields = self.get_fields(value)
            return "{" + ", ".join([f"{field}: {self.serialize_value(getattr(value, field))}" for field in fields]) + "}"
        else:
            return str(value)