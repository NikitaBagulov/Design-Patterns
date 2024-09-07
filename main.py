import json
import os

        
"""
Настройки
"""
class settings:
    __organization_name = ""
    __inn = ""

    @property
    def organization_name(self):
        return self.__organization_name
    

    @organization_name.setter
    def organization_name(self, value:str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр!")
        
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn

    def inn(self, value:str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")

        self.__inn = value


"""
Менеджер настроек
"""
class settings_manager:
    __file_name = "settings.json"
    __settings:settings = None


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance 
     

    def __init__(self) -> None:
        if self.__settings is None:
            self.__settings = self.__default_setting() 

    """
    Открыть и загрузить настройки
    """
    def open(self, file_name:str = ""):
        if not isinstance(file_name, str):
            raise TypeError("Некорректно переданы параметры!")
        
        if file_name != "":
            self.__file_name = file_name

        try:
            full_name = f"{os.curdir}{os.sep}{self.__file_name}"
            stream = open(full_name)
            data = json.load(stream)


            # Список полей от типа назначения    
            fields = list(filter(lambda x: not x.startswith("_"), dir(self.__settings.__class__)))

            # Заполняем свойства 
            for field in fields:
                keys = list(filter(lambda x: x == field, data.keys()))
                if len(keys) != 0:
                    value = data[field]

                    # Если обычное свойство - заполняем.
                    if not isinstance(value, list) and not isinstance(value, dict):
                        setattr(self.__settings, field, value)

            return True
        except:
            self.__settings = self.__default_setting()
            return False

    """
    Загруженные настройки
    """
    @property
    def settings(self):
        return self.__settings
    
    """
    Набор настроек по умолчанию
    """
    def __default_setting(self):
        data = settings()
        data.inn = "380080920202"
        data.organization_name = "Рога и копыта (default)"

        return data


manager1 = settings_manager()
if not manager1.open("settings.json"):
    print("Настройки не загружены!")

print(f"settings1: {manager1.settings.organization_name}")

manager2 = settings_manager()
print(f"settings2: {manager2.settings.organization_name}")

# 1 При отключенном методе __new__
# settings1: Рога и копыта
# settings2: Рога и копыта (default)

# 2 При включенном методе __new__
# settings1: Рога и копыта
# settings2: Рога и копыта