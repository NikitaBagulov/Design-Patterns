import json
import os
from src.models.settings import settings
from src.core.abstract_logic import abstract_logic
from src.core.format_reporting import format_reporting
from src.utils.validator import Validator
from src.utils.custom_exceptions import ConversionException, NotFoundException, ArgumentException, LengthException

class settings_manager(abstract_logic):
    __file_name = "settings.json"
    __settings: settings = None
    __report_settings = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance 

    def __init__(self) -> None:
        if self.__settings is None:
            self.__settings = self.__default_setting()
        self.__load_report_settings()

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
            self.__settings.__report_settings = self.__report_settings
        except json.JSONDecodeError:
            self.set_exception(ArgumentException("settings", "Ошибка декодирования JSON"))
        except Exception as e:
            self.set_exception(ArgumentException("settings", str(e)))

    def convert(self, data: dict):
        for key, value in data.items():
            if hasattr(self.__settings, key):
                try:
                    setattr(self.__settings, key, value)
                except (ValueError) as e:
                    self.set_exception(e)
                    raise ConversionException("Ошибка при конвертации данных.") from e

    def open(self, file_name: str = ""):
        Validator.validate_non_empty(file_name, "file_name")

        if file_name != "":
            self.__file_name = file_name

        try:
            full_path = self.__get_file_path(self.__file_name)
            if not full_path:
                self.__settings = self.__default_setting()
                raise NotFoundException(self.__file_name)
            
            with open(full_path, encoding="utf-8") as stream:
                data = json.load(stream)
                self.convert(data)

            return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.set_exception(e)
            self.__settings = self.__default_setting()
            return False
        except Exception as e:
            self.set_exception(e)
            return False

    @property
    def settings(self):
        return self.__settings

    def __default_setting(self):
        data = settings()
        try:
            Validator.validate_non_empty("Рога и копыта (default)", "organization_name")
            Validator.validate_digits("380080920202", 12, "inn")
            Validator.validate_digits("12345678901", 11, "account")
            Validator.validate_digits("09876543211", 11, "corr_account")
            Validator.validate_digits("123456789", 9, "bik")
            Validator.validate_length("Частн", 5, "ownership_type")

            data.organization_name = "Рога и копыта (default)"
            data.inn = "380080920202"
            data.account = "12345678901"
            data.corr_account = "09876543211"
            data.bik = "123456789"
            data.ownership_type = "Частн"
        except (ValueError, ArgumentException, LengthException) as e:
            self.set_exception(e)
            raise ConversionException("Ошибка при установке значений по умолчанию.") from e
        return data
    
    @staticmethod
    def __get_file_path(filename, search_path=os.curdir):
        for root, dirs, files in os.walk(search_path):
            full_path = os.path.join(root, filename)
            if os.path.isfile(full_path):
                return full_path
        return None
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
