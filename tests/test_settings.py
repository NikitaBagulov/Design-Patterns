import unittest
from src.settings_manager import settings_manager

class test_settings(unittest.TestCase):
    def test_settings_manager_open_fail(self):
       manager1 = settings_manager()
       manager1.open("../settings1.json")
       print(manager1.error_text)
       assert manager1.is_error == True

    def test_settings_manager_open(self):
       manager1 = settings_manager()
       result = manager1.open("../settings.json")
       assert result is True

    def test_settings_manager_singletone(self):
       manager1 = settings_manager()
       result = manager1.open("../settings.json")
       manager2 = settings_manager()

       assert manager1 == manager2
       assert manager1.settings.inn == manager2.settings.inn
       assert manager1.settings.organization_name == manager2.settings.organization_name

       

if __name__ == '__main__':
    unittest.main()   