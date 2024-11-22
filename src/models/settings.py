from src.utils.validator import Validator
from src.core.format_reporting import format_reporting
from datetime import datetime
from src.core.event_type import event_type
from src.logics.observe_service import observe_service

class settings:
    def __init__(self):
        self.__organization_name = ""
        self.__inn = ""
        self.__account = ""
        self.__corr_account = ""
        self.__bik = ""
        self.__ownership_type = ""
        self.__report_format = format_reporting.CSV
        self.__report_settings: dict = None
        self.block_period: datetime
        self.__first_start: bool = True
        self.__min_log_level = ""
        self.__log_to_file = True
        self.__log_file_path = ""

    @property
    def organization_name(self):
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, value: str):
        try:
            Validator.validate_non_empty(value, "organization_name")
            Validator.validate_length(value, 255, "organization_name")
            self.__organization_name = value
            observe_service.raise_event(event_type.INFO, {"message": f"Organization name set to: {value}"})
        except Exception as e:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting organization_name: {str(e)}"})
            raise

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        try:
            Validator.validate_digits(value, 12, "ИНН")
            self.__inn = value
            observe_service.raise_event(event_type.INFO, {"message": f"INN set to: {value}"})
        except Exception as e:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting INN: {str(e)}"})
            raise

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value: str):
        try:
            Validator.validate_digits(value, 11, "Счет")
            self.__account = value
            observe_service.raise_event(event_type.INFO, {"message": f"Account set to: {value}"})
        except Exception as e:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting account: {str(e)}"})
            raise

    @property
    def corr_account(self):
        return self.__corr_account

    @corr_account.setter
    def corr_account(self, value: str):
        try:
            Validator.validate_digits(value, 11, "Корреспондентский счет")
            self.__corr_account = value
            observe_service.raise_event(event_type.INFO, {"message": f"Correspondent account set to: {value}"})
        except Exception as e:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting correspondent account: {str(e)}"})
            raise

    @property
    def bik(self):
        return self.__bik

    @bik.setter
    def bik(self, value: str):
        try:
            Validator.validate_digits(value, 9, "БИК")
            self.__bik = value
            observe_service.raise_event(event_type.INFO, {"message": f"Bik set to: {value}"})
        except Exception as e:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting bik: {str(e)}"})
            raise

    @property
    def ownership_type(self):
        return self.__ownership_type

    @ownership_type.setter
    def ownership_type(self, value: str):
        try:
            Validator.validate_non_empty(value, "ownership_type")
            Validator.validate_length(value, 5, "Форма собственности")
            self.__ownership_type = value
            observe_service.raise_event(event_type.INFO, {"message": f"Ownership type set to: {value}"})
        except Exception as e:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting ownership_type: {str(e)}"})
            raise

    @property
    def report_format(self):
        return self.__report_format

    @report_format.setter
    def report_format(self, value: str):
        try:
            Validator.validate_enum_value(value, format_reporting, "ReportFormat")
            self.__report_format = value
            observe_service.raise_event(event_type.INFO, {"message": f"Report format set to: {value}"})
        except Exception as e:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting report format: {str(e)}"})
            raise

    @property
    def block_period(self):
        return self.__block_period

    @block_period.setter
    def block_period(self, value: str):
        try:
            Validator.validate_length(value, 12, "block_period")
            self.__block_period = datetime.strptime(value, "%Y-%m-%d")
            observe_service.raise_event(event_type.INFO, {"message": f"Block period set to: {value}"})
        except Exception as e:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting block_period: {str(e)}"})
            raise

    @property
    def first_start(self):
        return self.__first_start

    @first_start.setter
    def first_start(self, value: bool):
        try:
            Validator.validate_type(value, bool, "first_start")
            self.__first_start = value
            observe_service.raise_event(event_type.INFO, {"message": f"First start set to: {value}"})
        except Exception as e:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting first_start: {str(e)}"})
            raise

    @property
    def min_log_level(self):
        return self.__min_log_level

    @min_log_level.setter
    def min_log_level(self, value: str):
        try:
            Validator.validate_type(value, str, "min_log_level")
            self.__min_log_level = value
            observe_service.raise_event(event_type.INFO, {"message": f"Min log level set to: {value}"})
        except Exception as e:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting min_log_level: {str(e)}"})
            raise

    @property
    def log_to_file(self):
        return self.__log_to_file

    @log_to_file.setter
    def log_to_file(self, value: bool):
        try:
            Validator.validate_type(value, bool, "log_to_file")
            self.__log_to_file = value
            observe_service.raise_event(event_type.INFO, {"message": f"Log to file set to: {value}"})
        except Exception as e:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting log_to_file: {str(e)}"})
            raise

    @property
    def log_file_path(self):
        return self.__log_file_path

    @log_file_path.setter
    def log_file_path(self, value: str):
        try:
            Validator.validate_type(value, str, "log_file_path")
            self.__log_file_path = value
            observe_service.raise_event(event_type.INFO, {"message": f"Log file path set to: {value}"})
        except Exception as e:
            observe_service.raise_event(event_type.ERROR, {"message": f"Error setting log_file_path: {str(e)}"})
            raise


