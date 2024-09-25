import json
from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
from src.utils.validator import Validator

class json_report(abstract_report):
    
    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.JSON

    @staticmethod
    def serialize_object(obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        else:
            row_data = {}
            fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(obj.__class__, x)), dir(obj)))
            for field in fields:
                value = getattr(obj, field)
                if isinstance(value, list):
                    row_data[field] = [json_report.serialize_object(v) for v in value]
                elif hasattr(value, '__dict__'):
                    row_data[field] = json_report.serialize_object(value)
                else:
                    row_data[field] = value
            return row_data

    def create(self, data: list):
        Validator.validate_type(data, list, "data")
        report_data = [self.serialize_object(row) for row in data]
        self.result = json.dumps(report_data, ensure_ascii=False, indent=4)
