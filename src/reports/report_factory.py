from src.core.abstract_logic import abstract_logic
from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
from src.utils.validator import Validator
from src.utils.custom_exceptions import ArgumentException, NotFoundException  
import json 
import os
from importlib import import_module

class report_factory(abstract_logic):
    __reports: dict = {}
    __report_settings: dict = {} 

    def __init__(self) -> None:
        super().__init__()
        self.__load_report_settings()
        self.__initialize_reports()

    def __initialize_reports(self):
        for report_format, report_class_path in self.__report_settings.items():
            try:
                module_path, class_name = report_class_path.rsplit('.', 1)
                module = import_module(module_path)
                report_class = getattr(module, class_name)
                if not issubclass(report_class, abstract_report):
                    raise TypeError(f"{report_class} не является подклассом abstract_report")
                self.__reports[format_reporting[report_format]] = report_class
            except (ImportError, AttributeError, TypeError) as e:
                self.set_exception(ArgumentException("reports", str(e)))

    def __load_report_settings(self):
        reports_file = 'reports.json'
        full_path = self.__get_file_path(reports_file)

        if not full_path:
            self.set_exception(NotFoundException(reports_file))
            return
        
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                self.__report_settings = json.load(file)
            for key in self.__report_settings.keys():
                if key not in format_reporting.__members__:
                    raise ValueError(f"Неверный формат в настройках: {key}")
        except json.JSONDecodeError:
            self.set_exception(ArgumentException("settings", "Ошибка декодирования JSON"))
        except Exception as e:
            self.set_exception(ArgumentException("settings", str(e)))

    @staticmethod
    def __get_file_path(filename, search_path=os.curdir):
        """Ищет файл в указанном каталоге и его подкаталогах."""
        for root, dirs, files in os.walk(search_path):
            full_path = os.path.join(root, filename)
            if os.path.isfile(full_path):
                return full_path
        return None

    def create(self, format: format_reporting) -> abstract_report:
        Validator.validate_type(format, format_reporting, "format")
        if format not in self.__reports.keys():
            self.set_exception(ArgumentException("format", f"Указанный вариант формата '{format}' не реализован!"))
            return None
        
        report = self.__reports[format]
        return report()

    def create_default(self) -> abstract_report:
        default_format = format_reporting.CSV
        return self.create(default_format)
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)