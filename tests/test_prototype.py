import unittest
from src.logics.domain_prototype import domain_prototype
from src.dto.filter import filter
from src.data_reposity import data_reposity
from src.settings_manager import settings_manager
from src.utils.recipe_manager import recipe_manager
from src.start_service import start_service
from src.dto.filter_type import filter_type

"""
Набор тестов для проверки прототипов
"""
class test_prototype(unittest.TestCase):

    def setUp(self):
        # Подготовка
        self.reposity = data_reposity()
        self.manager = settings_manager()
        self.recipe_manager = recipe_manager()
        self.service = start_service(self.reposity, self.manager, self.recipe_manager)
        self.service.create()

        # Проверка наличия данных
        if len(self.reposity.data[data_reposity.nomenclature_key()]) == 0:
            raise Exception("Нет данных!")

    def test_prototype_nomenclature_by_name(self):
        """
        Тест фильтрации номенклатуры по полю 'name'.
        """
        data = self.reposity.data[data_reposity.nomenclature_key()]
        item = data[0]

        # Настройка фильтра
        filter_dto = filter(name=item.name, type = filter_type.EQUALS)
        prototype = domain_prototype(data)

        # Действие
        result = prototype.create(data, filter_dto)
        print(result.data)
        # Проверка
        assert len(result.data) == 1
        assert result.data[0] == item

    def test_prototype_nomenclature_by_unique_code(self):
        """
        Тест фильтрации номенклатуры по полю 'unique_code'.
        """
        data = self.reposity.data[data_reposity.nomenclature_key()]
        item = data[0]

        # Настройка фильтра
        filter_dto = filter(unique_code=item.unique_code)
        print(item.unique_code)
        prototype = domain_prototype(data)

        # Действие
        result = prototype.create(data, filter_dto)

        # Проверка
        assert len(result.data) == 1
        assert result.data[0] == item

    def test_prototype_nomenclature_by_like(self):
        """
        Тест фильтрации с использованием фильтра LIKE по полю 'name'.
        """
        data = self.reposity.data[data_reposity.nomenclature_key()]
        item = data[0]

        # Настройка фильтра с частичным совпадением
        filter_dto = filter(name=item.name[:3], type=filter_type.LIKE)
        prototype = domain_prototype(data)

        # Действие
        result = prototype.create(data, filter_dto)

        # Проверка
        assert len(result.data) > 0
        assert result.data[0].name.startswith(item.name[:3])

    def test_prototype_range_by_name(self):
        """
        Тест фильтрации range_model по полю 'name'.
        """
        data = self.reposity.data[data_reposity.range_key()]
        item = data[0]

        # Настройка фильтра
        filter_dto = filter(name=item.name, type=filter_type.EQUALS)
        print(item.name)
        prototype = domain_prototype(data)

        # Действие
        result = prototype.create(data, filter_dto)
        print(result.data)

        # Проверка
        assert len(result.data) == 2
        assert result.data[0] == item

    def test_prototype_range_by_like(self):
        """
        Тест фильтрации range_model с использованием фильтра LIKE по полю 'name'.
        """
        data = self.reposity.data[data_reposity.range_key()]
        item = data[0]

        # Настройка фильтра с частичным совпадением
        filter_dto = filter(name=item.name[:3], type=filter_type.LIKE)
        prototype = domain_prototype(data)

        # Действие
        result = prototype.create(data, filter_dto)

        # Проверка
        assert len(result.data) > 0
        assert result.data[0].name.startswith(item.name[:3])

    def test_prototype_group_by_name(self):
        """
        Тест фильтрации group_model по полю 'name'.
        """
        data = self.reposity.data[data_reposity.group_key()]
        item = data[0]

        # Настройка фильтра
        filter_dto = filter(name=item.name, type=filter_type.EQUALS)
        prototype = domain_prototype(data)

        # Действие
        result = prototype.create(data, filter_dto)

        # Проверка
        assert len(result.data) == 1
        assert result.data[0] == item

    def test_prototype_group_by_like(self):
        """
        Тест фильтрации group_model с использованием фильтра LIKE по полю 'name'.
        """
        data = self.reposity.data[data_reposity.group_key()]
        item = data[0]

        # Настройка фильтра с частичным совпадением
        filter_dto = filter(name=item.name[:3], type=filter_type.LIKE)
        prototype = domain_prototype(data)

        # Действие
        result = prototype.create(data, filter_dto)

        # Проверка
        assert len(result.data) > 0
        assert result.data[0].name.startswith(item.name[:3])

    def test_prototype_recipe_by_name(self):
        """
        Тест фильтрации recipe_model по полю 'name'.
        """
        data = self.reposity.data[data_reposity.recipes_key()]
        item = data[0]

        # Настройка фильтра
        filter_dto = filter(name=item.name, type=filter_type.EQUALS)
        prototype = domain_prototype(data)

        # Действие
        result = prototype.create(data, filter_dto)

        # Проверка
        assert len(result.data) == 1
        assert result.data[0] == item

    def test_prototype_recipe_by_unique_code(self):
        """
        Тест фильтрации recipe_model по полю 'unique_code'.
        """
        data = self.reposity.data[data_reposity.recipes_key()]
        item = data[0]

        # Настройка фильтра
        filter_dto = filter(unique_code=item.unique_code, type=filter_type.EQUALS)
        prototype = domain_prototype(data)

        # Действие
        result = prototype.create(data, filter_dto)

        # Проверка
        assert len(result.data) == 1
        assert result.data[0] == item
