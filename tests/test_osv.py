import unittest
from main import app  
from src.data_reposity import data_reposity
from src.settings_manager import settings_manager
from src.utils.recipe_manager import recipe_manager
from src.start_service import start_service
from src.reports.turnover_balance_sheet import turnover_balance_sheet
from flask import jsonify
from datetime import datetime

class test_osv(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.testing = True
        cls.client = cls.app.test_client()

        cls.reposity = data_reposity()
        cls.manager = settings_manager()
        cls.recipe_manager = recipe_manager()
        cls.service = start_service(cls.reposity, cls.manager, cls.recipe_manager)
        cls.balance_sheet = turnover_balance_sheet(cls.reposity)
        
    def test_get_osv_report_success(self):
        start_date = "2024-01-01"
        end_date = "2024-10-31"
        warehouse = "BESTWAREHOUSE"

        response = self.client.get("/api/report/osv", params={
            "start_date": start_date,
            "end_date": end_date,
            "warehouse": warehouse
        })
        print(response.text)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Remainders", data)
        self.assertIn("Receipts", data)
        self.assertIn("Opening remainders", data)
        self.assertIn("Consumptions", data)
    
    def test_get_osv_report_missing_parameters(self):

        response = self.client.get("/api/report/osv", params={})

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Отсутствуют обязательные параметры: 'start_date', 'end_date', or 'warehouse'")
    
    def test_save_repository_success(self):
        response = self.client.post("/api/repository/save")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Данные успешно сохранены в файл.")

    def test_restore_repository_success(self):
        response = self.client.post("/api/repository/restore")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Данные успешно восстановлены из файла.")
        
if __name__ == '__main__':
    unittest.main()
