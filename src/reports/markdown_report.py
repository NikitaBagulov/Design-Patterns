from src.core.format_reporting import format_reporting
from src.core.abstract_report import abstract_report
from src.utils.validator import Validator

class markdown_report(abstract_report):

    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.MARKDOWN

    def create(self, data: list):
        Validator.validate_type(data, list, "data")
        first_model = data[0]
       
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)), dir(first_model)))
        
        self.result += "| " + " | ".join(fields) + " |\n"
        self.result += "| " + " | ".join(["---"] * len(fields)) + " |\n"

        for row in data:
            row_values = [str(getattr(row, field)) for field in fields]
            self.result += "| " + " | ".join(row_values) + " |\n"
        print(self.result)