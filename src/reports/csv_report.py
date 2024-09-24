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
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x )),  dir(first_model) ))

        for field in fields:
            self.result += f"{str(field)};"

        self.result += "\n"    

        for row in data:
            for field in fields:
            
                value = getattr(row, field)
                self.result += f"{str(value)};"
            self.result += "\n"
        print(self.result)