import unittest
from src.start_service import start_service
from src.data_reposity import data_reposity
from src.settings_manager import settings_manager

class TestDataRepository(unittest.TestCase):

    def setUp(self):
        self.reposity = data_reposity()
        self.manager = settings_manager()
        self.service = start_service(self.reposity, self.manager)

    def test_data_created(self):
        self.service.create()

        self.assertIn(data_reposity.nomenclature_key(), self.reposity.data)
        self.assertGreater(len(self.reposity.data[data_reposity.nomenclature_key()]), 0)

        self.assertIn(data_reposity.group_key(), self.reposity.data)
        self.assertGreater(len(self.reposity.data[data_reposity.group_key()]), 0)

        self.assertIn(data_reposity.range_key(), self.reposity.data)
        self.assertGreater(len(self.reposity.data[data_reposity.range_key()]), 0)

        self.assertIn(data_reposity.recipes_key(), self.reposity.data)
        self.assertGreater(len(self.reposity.data[data_reposity.recipes_key()]), 0)

if __name__ == '__main__':
    unittest.main()