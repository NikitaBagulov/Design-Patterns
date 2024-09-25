from src.utils.validator import Validator
from src.core.format_reporting import format_reporting
from src.reports.csv_report import csv_report
from src.reports.markdown_report import markdown_report
from src.reports.json_report import json_report
from src.reports.xml_report import xml_report
from src.reports.rtf_report import rtf_report

class settings:
    def __init__(self):
        self.__organization_name = ""
        self.__inn = ""
        self.__account = ""
        self.__corr_account = ""
        self.__bik = ""
        self.__ownership_type = ""
        self.__report_format = format_reporting.CSV

    @property
    def organization_name(self):
        return self.__organization_name
    
    @organization_name.setter
    def organization_name(self, value: str):
        Validator.validate_non_empty(value, "organization_name")
        Validator.validate_length(value, 255, "organization_name")
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn
    
    @inn.setter
    def inn(self, value: str):
        Validator.validate_digits(value, 12, "ИНН")
        self.__inn = value

    @property
    def account(self):
        return self.__account
    
    @account.setter
    def account(self, value: str):
        Validator.validate_digits(value, 11, "Счет")
        self.__account = value

    @property
    def corr_account(self):
        return self.__corr_account
    
    @corr_account.setter
    def corr_account(self, value: str):
        Validator.validate_digits(value, 11, "Корреспондентский счет")
        self.__corr_account = value

    @property
    def bik(self):
        return self.__bik
    
    @bik.setter
    def bik(self, value: str):
        Validator.validate_digits(value, 9, "БИК")
        self.__bik = value

    @property
    def ownership_type(self):
        return self.__ownership_type
    
    @ownership_type.setter
    def ownership_type(self, value: str):
        Validator.validate_non_empty(value, "ownership_type")
        Validator.validate_length(value, 5, "Форма собственности")
        self.__ownership_type = value

    @property
    def report_format(self):
        return self.__report_format

    @report_format.setter
    def report_format(self, value: str):
        Validator.validate_enum_value(value, format_reporting, "ReportFormat")
        self.__report_format = value

    def get_report_instance(self):

        format_to_class_map = {
            "CSV": csv_report,
            "Markdown": markdown_report,
            "Json": json_report,
            "XML": xml_report,
            "RTF": rtf_report
        }

        report_class = format_to_class_map.get(self.__report_format)
        if report_class:
            return report_class()
        else:
            Validator.validate_enum_value(self.__report_format, format_reporting, "ReportFormat")
