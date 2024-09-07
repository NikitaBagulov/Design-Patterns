import json
import os
from settings import settings

def find_file(filename, search_path=os.curdir):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

class settings_manager:
    __file_name = "settings.json"
    __settings: settings = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance 

    def __init__(self) -> None:
        if self.__settings is None:
            self.__settings = self.__default_setting()

    def convert(self, data: dict):
        for key, value in data.items():
            if hasattr(self.__settings, key):
                setattr(self.__settings, key, value)

    def open(self, file_name: str = ""):
        if not isinstance(file_name, str):
            raise TypeError("Некорректно переданы параметры!")
        
        if file_name != "":
            self.__file_name = file_name

        try:
            full_name = find_file(self.__file_name)
            if not full_name:
                self.__settings = self.__default_setting()
                raise FileNotFoundError(f"Файл {self.__file_name} не найден в текущем или дочерних каталогах.")
            
            print(full_name)
            with open(full_name, encoding="utf-8") as stream:
                data = json.load(stream)
                print(data)
                self.convert(data)

            return True
        except Exception as e:
            print(f"Ошибка загрузки файла: {e}")
            self.__settings = self.__default_setting()
            return False

    @property
    def settings(self):
        return self.__settings

    def __default_setting(self):
        data = settings()
        data.organization_name = "Рога и копыта (default)"
        data.inn = "380080920202"
        data.account = "12345678901"
        data.corr_account = "09876543211"
        data.bik = "123456789"
        data.ownership_type = "Частн"
        return data