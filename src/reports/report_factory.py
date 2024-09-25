from src.core.abstract_logic import abstract_logic
from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
from src.reports.csv_report import csv_report
from src.reports.markdown_report import markdown_report
from src.reports.json_report import json_report
from src.reports.xml_report import xml_report
from src.reports.rtf_report import rtf_report
from src.utils.validator import Validator
from src.utils.custom_exceptions import ArgumentException
from src.settings_manager import settings_manager
import json

class report_factory(abstract_logic):
    __reports: dict = {
        format_reporting.CSV: csv_report,
        format_reporting.MARKDOWN: markdown_report,
        format_reporting.JSON: json_report,
        format_reporting.XML: xml_report,
        format_reporting.RTF: rtf_report
    }

    def __init__(self) -> None:
        super().__init__()
        self.__report_settings = settings_manager().settings.report_settings

    def create(self, format: format_reporting) -> abstract_report:
        Validator.validate_type(format, format_reporting, "format")
        if format not in self.__reports.keys():
            self.set_exception(ArgumentException("format", f"Указанный вариант формата '{format}' не реализован!"))
            return None
        
        report_class = self.__reports[format]
        return report_class()

    def create_default(self) -> abstract_report:
        default_format = format_reporting.CSV
        return self.create(default_format)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
