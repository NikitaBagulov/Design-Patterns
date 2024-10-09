import unittest
from src.logics.nomenclature_prototype import nomenclature_prototype
from src.dto.filter import filter
from src.data_reposity import data_reposity
from src.settings_manager import settings_manager
from src.utils.recipe_manager import recipe_manager
from src.start_service import start_service

"""
Набор тестов для проверки прототипов
"""
class test_prototype(unittest.TestCase):

    def test_prototype_nomenclature(self):
        # Подготовка
        self.reposity = data_reposity()
        self.manager = settings_manager()
        self.recipe_manager = recipe_manager()
        self.service = start_service(self.reposity, self.manager, self.recipe_manager)
        self.service.create()
        
        if len( self.reposity.data[ data_reposity.nomenclature_key()]) == 0:
            raise Exception("Нет данных!")
        
        data = self.reposity.data[ data_reposity.nomenclature_key()  ]
        item = data[0]
        item_filter = filter()
        item_filter.name = item.name
        prototype = nomenclature_prototype(  data )


        # Действие
        result = prototype.create( data, item_filter)

        # Проверка
        assert len(result.data) == 1
        assert result.data[0] ==  item
