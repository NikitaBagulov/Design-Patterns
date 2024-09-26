from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.utils.validator import Validator

class csv_report(abstract_report):

    def __init__(self) -> None:
       super().__init__()
       self.__format = format_reporting.CSV

    def create(self, data: list):
        Validator.validate_type(data, list, "data")
        
        if not data:
            return

        first_model = data[0]
        fields = self.get_fields(first_model)

        for field in fields:
            self.result += f"{str(field)};"
        self.result += "\n"

        for row in data:
            for field in fields:
                value = getattr(row, field)
                self.result += f"{self.serialize_value(value)};"
            self.result += "\n"

    def get_fields(self, obj):
        """Получаем список полей модели, исключая приватные и callable-атрибуты"""
        return list(filter(lambda x: not x.startswith("_") and not callable(getattr(obj.__class__, x)), dir(obj)))

    def serialize_value(self, value):
        """Сериализация только простых значений для CSV (без вложенных объектов, списков и словарей)"""
        if isinstance(value, (int, float, str)):
            return str(value)
        elif hasattr(value, "__dict__"):
            fields = self.get_fields(value)
            simple_values = []
            for field in fields:
                field_value = getattr(value, field)
                if isinstance(field_value, (int, float, str)):
                    simple_values.append(str(field_value))
            return "; ".join(simple_values)
        else:
            return ""