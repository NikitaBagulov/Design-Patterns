import unittest
from src.models.range import range_model
from src.models.nomenclature import nomenclature_model
from src.models.company import company_model
from src.models.warehouse import warehouse_model
from src.settings_manager import settings_manager
from src.utils.custom_exceptions import ArgumentException, ConversionException

class test_models(unittest.TestCase):

    def test_nomenclature_model_creation(self):
        """Тест создания объекта номенклатуры и проверка полей."""
        item = nomenclature_model()
        item.name = "test1"
        item.full_name = "Test Item 1"

        self.assertEqual(item.name, "test1")
        self.assertEqual(item.full_name, "Test Item 1")

    def test_nomenclature_model_unique_code(self):
        """Тест уникального кода для объектов номенклатуры."""
        item1 = nomenclature_model()
        item1.name = "test1"

        item2 = nomenclature_model()
        item2.name = "test1"

        self.assertNotEqual(item1, item2)

    def test_nomenclature_model_full_name_validation(self):
        """Тест валидации для полного имени номенклатуры."""
        item = nomenclature_model()

        with self.assertRaises(ArgumentException):
            item.full_name = "x" * 256

    def test_range_model_creation(self):
        """Тест создания и установки полей для единицы измерения."""
        item = range_model()
        item.name = "test1"

        self.assertEqual(item.name, "test1")

    def test_range_model_base_unit(self):
        """Тест установки базовой единицы и коэффициента пересчета для единицы измерения."""
        base_range = range_model()
        base_range.name = "грамм"

        new_range = range_model()
        new_range.name = "кг"
        new_range.set_base_unit(base_range, 1000)

        self.assertEqual(new_range.base_unit.name, "грамм")
        self.assertEqual(new_range.conversion_factor, 1000)

    def test_range_model_conversion_exceptions(self):
        """Тест исключений при некорректной установке базовой единицы и коэффициента пересчета."""
        base_range = range_model()
        base_range.name = "грамм"

        new_range = range_model()
        new_range.name = "кг"

        with self.assertRaises(ValueError):
            new_range.set_base_unit(base_range, -1)

        with self.assertRaises(ArgumentException):
            new_range.set_base_unit("invalid_base", 1000)

    def test_company_model_loading_settings(self):
        """Тест загрузки настроек в модель компании и проверки полей."""
        manager = settings_manager()
        manager.open("settings.json")

        company = company_model()
        company.load_from_settings(manager.settings)

        self.assertEqual(company.inn, manager.settings.inn)
        self.assertEqual(company.bik, manager.settings.bik)
        self.assertEqual(company.account, manager.settings.account)
        self.assertEqual(company.ownership_type, manager.settings.ownership_type)

    def test_company_model_inn_validation(self):
        """Тест валидации ИНН в модели компании."""
        company = company_model()

        with self.assertRaises(ArgumentException):
            company.inn = "12345678910111"

    def test_company_model_bik_validation(self):
        """Тест валидации БИК в модели компании."""
        company = company_model()

        with self.assertRaises(ArgumentException):
            company.bik = "12345"

    def test_company_model_account_validation(self):
        """Тест валидации счета в модели компании."""
        company = company_model()

        with self.assertRaises(ArgumentException):
            company.account = "12345"

    def test_company_model_ownership_type_validation(self):
        """Тест валидации вида собственности в модели компании."""
        company = company_model()

        with self.assertRaises(ArgumentException):
            company.ownership_type = "TTTRRRRRRRRRRR"

    def test_warehouse_model_creation(self):
        """Тест создания и установки полей для модели склада."""
        warehouse = warehouse_model()
        warehouse.name = "Main Warehouse"
        warehouse.address = "123 Main St"

        self.assertEqual(warehouse.name, "Main Warehouse")
        self.assertEqual(warehouse.address, "123 Main St")

    def test_warehouse_model_comparison(self):
        """Тест сравнения двух объектов склада."""
        warehouse1 = warehouse_model()
        warehouse1.name = "Main Warehouse"
        warehouse1.address = "123 Main St"

        warehouse2 = warehouse_model()
        warehouse2.name = "Backup Warehouse"
        warehouse2.address = "456 Backup Ave"

        self.assertNotEqual(warehouse1, warehouse2)

    def test_warehouse_model_empty_values(self):
        """Тест работы модели склада с пустыми значениями."""
        warehouse = warehouse_model()
        warehouse.name = ""
        warehouse.address = ""

        self.assertEqual(warehouse.name, "")
        self.assertEqual(warehouse.address, "")

if __name__ == '__main__':
    unittest.main()
