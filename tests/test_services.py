import unittest
from main import app  # Импортируйте приложение Flask из main.py
from src.logics.nomenclature_service import nomenclature_service
from src.core.event_type import event_type
from src.data_reposity import data_reposity
from src.models.nomenclature import nomenclature_model
from src.settings_manager import settings_manager
from src.utils.recipe_manager import recipe_manager
from src.start_service import start_service

class TestNomenclatureService(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.testing = True
        cls.client = cls.app.test_client()
        cls.reposity = data_reposity()
        cls.manager = settings_manager()
        cls.recipe_manager = recipe_manager()
        cls.service = start_service(cls.reposity, cls.manager, cls.recipe_manager)
    
    def test_get_nomenclature(self):
        """Тест для GET /api/nomenclature"""
        response = self.client.get('/api/nomenclature', params={'unique_code': self.reposity.data[data_reposity.nomenclature_key()][0].unique_code})

        data = response.json()

        if "error" in data:
            self.assertEqual(response.status_code, 404)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)

    def test_add_nomenclature(self):
        """Тест для PUT /api/nomenclature"""
        response = self.client.put('/api/nomenclature', json={
            'name': 'Еда',
            'full_name': 'Еда',
            'group_id': self.reposity.data[data_reposity.group_key()][0].unique_code,
            'range_id': self.reposity.data[data_reposity.range_key()][0].unique_code
        })
        data = response.json()
        if "status" in data:
            self.assertEqual(response.status_code, 400)
        else:
            self.assertIn('unique_code', data[0])

    def test_update_nomenclature(self):
        """Тест для PATCH /api/nomenclature"""
        response = self.client.patch('/api/nomenclature', json={
            'unique_code': self.reposity.data[data_reposity.nomenclature_key()][0].unique_code,
            'name': 'Updated Nomenclature'
        })
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", data)
        self.assertEqual(data["status"], "Номенклатура успешно обновлена")

    def test_delete_nomenclature(self):
        """Тест для DELETE /api/nomenclature"""
        response = self.client.delete('/api/nomenclature', params={'unique_code': self.reposity.data[data_reposity.nomenclature_key()][0].unique_code}, headers={'Content-Type': 'application/json'})
        data = response.json()

        if "status" in data:
            self.assertEqual(response.status_code, 400)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertIn("status", data)
            self.assertEqual(data["status"], "Номенклатура успешно удалена")
    
if __name__ == '__main__':
    unittest.main()
