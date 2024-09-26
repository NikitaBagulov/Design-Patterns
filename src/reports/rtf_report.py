from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
from src.utils.validator import Validator

class rtf_report(abstract_report):

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.RTF

    def create(self, data: list):
        Validator.validate_type(data, list, "data")

        rtf_content = r"{\rtf1\ansi\deff0"
        
        for row in data:
            rtf_content += r"\pard "
            rtf_content += self.serialize_object(row)
            rtf_content += r"\par "
        
        rtf_content += r"}"
        self.result = rtf_content

    def serialize_object(self, obj):
        result = ""
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(obj.__class__, x)), dir(obj)))

        for field in fields:
            value = getattr(obj, field)
            if isinstance(value, list):
                result += r"\b " + field + r":\b0 " + ", ".join([self.serialize_object(v) for v in value]) + r"\par "
            elif hasattr(value, '__dict__'):
                result += r"\b " + field + r":\b0 {\par " + self.serialize_object(value) + r"}\par "
            else:
                result += r"\b " + field + r":\b0 " + str(value) + r"\par "
        
        return result
