import json
import os
from src.models.settings import settings
from src.core.abstract_logic import abstract_logic
from src.core.format_reporting import format_reporting
from src.utils.validator import Validator
from src.utils.custom_exceptions import ConversionException, NotFoundException, ArgumentException, LengthException
from src.core.event_type import event_type
from src.logics.observe_service import observe_service

class settings_manager(abstract_logic):
    __file_name = "settings.json"
    __settings: settings = None
    __report_settings = {}
    

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance 

    def __init__(self) -> None:
        observe_service.append(self)
        if self.__settings is None:
            self.__settings = self.__default_setting()
        if not self.__settings.first_start:
            observe_service.raise_event(event_type.LOAD_REPOSITY, {})
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
            self.settings.report_settings = self.__report_settings
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

    @property
    def report_settings(self):
        return self.__report_settings

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
            data.block_period = "2024-01-01"
            data.first_start = True
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

    def save(self):
        if self.__settings.first_start:
            self.__settings.first_start = False
        required_attributes = [
            'organization_name', 'inn', 'account', 'corr_account', 
            'bik', 'ownership_type', 'block_period', 'first_start'
        ]
        
        for attr in required_attributes:
            if not hasattr(self.__settings, attr):
                raise AttributeError(f"Свойство {attr} не найдено в настройках.")

        full_path = self.__get_file_path(self.__file_name)
        
        if not full_path:
            raise NotFoundException(self.__file_name)

        data_to_save = {
            "organization_name": self.__settings.organization_name,
            "inn": self.__settings.inn,
            "account": self.__settings.account,
            "corr_account": self.__settings.corr_account,
            "bik": self.__settings.bik,
            "ownership_type": self.__settings.ownership_type,
            "block_period": self.__settings.block_period.isoformat(),
            "first_start": self.__settings.first_start
        }

        try:
            with open(full_path, 'w', encoding='utf-8') as file:
                json.dump(data_to_save, file, ensure_ascii=False, indent=4)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.set_exception(e)
            raise ConversionException("Ошибка при сохранении данных в файл.") from e
        
    def handle_event(self, type: event_type, params ):
        super().handle_event(type, params)
        if type == event_type.CHANGE_BLOCK_PERIOD:
            self.save()

