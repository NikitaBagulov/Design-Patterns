import unittest
from datetime import datetime
from src.models.warehouse import warehouse_model
from src.models.nomenclature import nomenclature_model
from src.models.range import range_model
from src.models.warehouse_transaction import warehouse_transaction_model
from src.models.warehouse_turnover import warehouse_turnover_model
from src.processors.warehouse_turnover_process import warehouse_turnover_process
from src.logics.warehouse_transaction_prototype import warehouse_transaction_prototype
from src.data_reposity import data_reposity
from src.settings_manager import settings_manager
from src.utils.recipe_manager import recipe_manager
from src.start_service import start_service
from src.dto.filter_dto import filter_dto, warehouse_nomenclature_filter_dto

class TestWarehouseTurnoverProcess(unittest.TestCase):

    def setUp(self):
        # Подготовка тестовых данных
        self.reposity = data_reposity()
        self.manager = settings_manager()
        self.recipe_manager = recipe_manager()
        self.service = start_service(self.reposity, self.manager, self.recipe_manager)
        self.service.create()

        # Проверка наличия данных
        if len(self.reposity.data[data_reposity.nomenclature_key()]) == 0:
            raise Exception("Нет данных!")

        # Задаем фиксированные склады и номенклатуры
        self.warehouse_1 = self.reposity.data[data_reposity.warehouses_key()][0]
        self.warehouse_2 = self.reposity.data[data_reposity.warehouses_key()][1]

        self.nomenclature_1 = self.reposity.data[data_reposity.nomenclature_key()][0]
        self.nomenclature_2 = self.reposity.data[data_reposity.nomenclature_key()][1]

        self.range_1 = self.reposity.data[data_reposity.range_key()][0]
        self.range_2 = self.reposity.data[data_reposity.range_key()][1]

        # Генерация фиксированных транзакций для тестирования
        self.transactions = [
            # Транзакции для склада 1
            warehouse_transaction_model.create(period=datetime(2024, 10, 23, 12, 12, 0), warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, range=self.range_1, quantity=100, is_incoming=True),
            warehouse_transaction_model.create(period=datetime(2024, 10, 23, 12, 55, 0), warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, range=self.range_1, quantity=50, is_incoming=False),
            warehouse_transaction_model.create(period=datetime(2024, 10, 23, 15, 0, 0), warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, range=self.range_1, quantity=25, is_incoming=False),

            # Транзакции для склада 2
            warehouse_transaction_model.create(period=datetime(2024, 10, 23), warehouse=self.warehouse_2, nomenclature=self.nomenclature_2, range=self.range_2, quantity=200, is_incoming=True),
            warehouse_transaction_model.create(period=datetime(2024, 10, 24), warehouse=self.warehouse_2, nomenclature=self.nomenclature_2, range=self.range_2, quantity=100, is_incoming=False),
        ]

    def test_turnover_within_period(self):
        # Применяем фильтрацию данных по периоду
        prototype = warehouse_transaction_prototype(self.transactions)
        filt = warehouse_nomenclature_filter_dto(
            period={'start': '2024-10-23', 'end': '2024-10-25'}
        )
        filtered_data = prototype.create(self.transactions, filt)

        # После фильтрации передаем данные в процесс
        process = warehouse_turnover_process()
        result = process.process(transactions=filtered_data.data)

        expected_turnovers = [
            warehouse_turnover_model.create(warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, range=self.range_1),
            warehouse_turnover_model.create(warehouse=self.warehouse_2, nomenclature=self.nomenclature_2, range=self.range_2),
        ]

        expected_turnovers[0].turnover = 100 - 50 - 25
        expected_turnovers[1].turnover = 200 - 100

        self.assertEqual(len(result), len(expected_turnovers))
        for expected, actual in zip(expected_turnovers, result):
            self.assertEqual(expected.warehouse, actual.warehouse)
            self.assertEqual(expected.nomenclature, actual.nomenclature)
            self.assertEqual(expected.range, actual.range)
            self.assertEqual(expected.turnover, actual.turnover)

    def test_turnover_without_filter(self):
        # Проверка расчета оборота без фильтров
        prototype = warehouse_transaction_prototype(self.transactions)
        filtered_data = prototype.create(self.transactions, warehouse_nomenclature_filter_dto())
        
        process = warehouse_turnover_process()
        result = process.process(transactions=filtered_data.data)

        self.assertGreater(len(result), 0)

    def test_turnover_with_warehouse_filter(self):
        # Проверка расчета оборота с фильтром по складу
        prototype = warehouse_transaction_prototype(self.transactions)
        filt = warehouse_nomenclature_filter_dto(
            warehouse=filter_dto(name=self.warehouse_1.name)
        )
        filtered_data = prototype.create(self.transactions, filt)

        process = warehouse_turnover_process()
        result = process.process(transactions=filtered_data.data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].warehouse, self.warehouse_1)

    def test_turnover_with_nomenclature_filter(self):
        # Проверка расчета оборота с фильтром по номенклатуре
        prototype = warehouse_transaction_prototype(self.transactions)
        filt = warehouse_nomenclature_filter_dto(
            nomenclature=filter_dto(name=self.nomenclature_2.name)
        )
        filtered_data = prototype.create(self.transactions, filt)

        process = warehouse_turnover_process()
        result = process.process(transactions=filtered_data.data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].nomenclature, self.nomenclature_2)

    def test_turnover_with_combined_filters(self):
        # Проверка расчета оборота с комбинированными фильтрами
        prototype = warehouse_transaction_prototype(self.transactions)
        filt = warehouse_nomenclature_filter_dto(
            warehouse=filter_dto(name=self.warehouse_2.name),
            nomenclature=filter_dto(name=self.nomenclature_2.name)
        )
        filtered_data = prototype.create(self.transactions, filt)

        process = warehouse_turnover_process()
        result = process.process(transactions=filtered_data.data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].warehouse, self.warehouse_2) 
        self.assertEqual(result[0].nomenclature, self.nomenclature_2) 
if __name__ == '__main__':
    unittest.main()
