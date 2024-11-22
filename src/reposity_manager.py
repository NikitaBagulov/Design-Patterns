import json
import os
from src.data_reposity import data_reposity
from src.core.abstract_logic import abstract_logic
from src.settings_manager import settings_manager
from src.reports.report_factory import report_factory
from src.core.format_reporting import format_reporting
from src.logics.observe_service import observe_service
from src.core.event_type import event_type

class reposity_manager(abstract_logic):
    def __init__(self, reposity: data_reposity, manager:settings_manager,  file_path: str = "repository_data.json"):
        self.reposity = reposity
        self.file_path = file_path
        self.manager = manager
        observe_service.append(self)
        

    def save_to_file(self):
        """
        Сохраняет текущие данные репозитория в файл в формате JSON.
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                report = report_factory(self.manager).create(format_reporting.JSON)
                data_to_save = {}
                for key, item in self.reposity.data.items():
                    report.create(item)
                    data_to_save[key] = report.result
                json.dump(data_to_save, file, ensure_ascii=False, indent=4)
        except Exception as e:
            raise Exception(f"Ошибка при сохранении данных в файл: {e}")

    def restore_from_file(self):
        """
        Восстанавливает данные репозитория из файла.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError("Файл данных не найден. Пожалуйста, сохраните данные перед восстановлением.")

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data_loaded = json.load(file)
                for key, item_data in data_loaded.items():
                    if isinstance(item_data, str):
                        item_data = json.loads(item_data)
                    item_instance = self.reposity.create_item(key)
                    result = [item_instance().deserialize(item) for item in item_data]

                    self.reposity.data[key] = result
            print("Данные успешно восстановлены из файла.")
        except Exception as e:
            raise Exception(f"Ошибка при восстановлении данных из файла: {e}")

    def set_file_path(self, file_path: str):
        self.file_path = file_path

    def handle_event(self, type: str, params):
        super().handle_event(type, params)
        if event_type.SAVE_REPOSITY:
            self.save_to_file()
        elif event_type.LOAD_REPOSITY:
            self.restore_from_file

    def set_exception(self, ex: Exception):
        return super().set_exception(ex)
