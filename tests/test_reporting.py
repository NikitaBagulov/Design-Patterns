from src.start_service import start_service
from src.settings_manager import settings_manager
from src.utils.recipe_manager import recipe_manager
from src.data_reposity import data_reposity
from src.reports.csv_report import csv_report
from src.reports.markdown_report import markdown_report
from src.reports.json_report import json_report
from src.reports.xml_report import xml_report
from src.reports.rtf_report import rtf_report
from src.reports.report_factory import report_factory
from src.core.format_reporting import format_reporting
from src.utils.json_deserializer import json_deserializer
from src.utils.custom_exceptions import ArgumentException


import json
import os
import unittest

class test_reporting(unittest.TestCase):
    

    def test_csv_report_create_range(self):
        manager = settings_manager()
        rec_manager = recipe_manager()
        reposity = data_reposity()
        start = start_service(reposity, manager, rec_manager)
        start.create()
        report = csv_report()

        # Действие
        report.create(reposity.data[ data_reposity.range_key()  ])

        # Проверки
        assert report.result != ""

    def test_csv_report_create_recipes(self):
        manager = settings_manager()
        rec_manager = recipe_manager()
        reposity = data_reposity()
        start = start_service(reposity, manager, rec_manager)
        start.create()
        report = csv_report()

        # Действие
        report.create(reposity.data[ data_reposity.recipes_key()  ])
        print(reposity.data[ data_reposity.recipes_key()])

        # Проверки
        assert report.result != ""


    def test_csv_report_create_nomenclature(self):
        manager = settings_manager()
        rec_manager = recipe_manager()
        reposity = data_reposity()
        start = start_service(reposity, manager, rec_manager)
        start.create()
        report = csv_report()

        # Действие
        report.create(reposity.data[ data_reposity.nomenclature_key()  ])

        # Проверки
        assert report.result != ""    

    def test_markdown_report_create_nomenclature(self):
        manager = settings_manager()
        rec_manager = recipe_manager()
        reposity = data_reposity()
        start = start_service(reposity, manager, rec_manager)
        start.create()
        report = markdown_report()

        # Действие
        report.create(reposity.data[ data_reposity.nomenclature_key()  ])

        # Проверки
        assert report.result != ""   

    def test_json_report_create_nomenclature(self):
        manager = settings_manager()
        rec_manager = recipe_manager()
        reposity = data_reposity()
        start = start_service(reposity, manager, rec_manager)
        start.create()
        report = json_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверки
        assert report.result != ""

    # Тест для XML отчета
    def test_xml_report_create_nomenclature(self):
        manager = settings_manager()
        rec_manager = recipe_manager()
        reposity = data_reposity()
        start = start_service(reposity, manager, rec_manager)
        start.create()
        report = xml_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверки
        assert report.result != ""

    # Тест для RTF отчета
    def test_rtf_report_create_nomenclature(self):
        manager = settings_manager()
        rec_manager = recipe_manager()
        reposity = data_reposity()
        start = start_service(reposity, manager, rec_manager)
        start.create()
        report = rtf_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверки
        assert report.result != ""

    def test_report_factory_create(self):
        manager = settings_manager()
        rec_manager = recipe_manager()
        reposity = data_reposity()
        start = start_service(reposity, manager, rec_manager)
        start.create()        

        report = report_factory(manager).create( format_reporting.CSV )

        assert report is not None
        assert isinstance(report,  csv_report)

    def test_report_factory_create_fail(self):
        manager = settings_manager()
        rec_manager = recipe_manager()
        reposity = data_reposity()
        start = start_service(reposity, manager, rec_manager)
        start.create()        
        factory = report_factory(manager)
       
        with self.assertRaises(ArgumentException):
            report = factory.create( "jfsojos" )

        
class test_reporting_generate_files(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.report_dir = os.path.join(os.path.dirname(__file__), 'reports')
        if not os.path.exists(cls.report_dir):
            os.makedirs(cls.report_dir)

        cls.manager = settings_manager()
        cls.rec_manager = recipe_manager()
        cls.reposity = data_reposity()
        cls.start = start_service(cls.reposity, cls.manager, cls.rec_manager)
        cls.start.create()

    def _save_report_to_file(self, report, filename):
        if isinstance(report, json_report):
            extension = 'json'
        elif isinstance(report, csv_report):
            extension = 'csv'
        elif isinstance(report, markdown_report):
            extension = 'md'
        elif isinstance(report, xml_report):
            extension = 'xml'
        elif isinstance(report, rtf_report):
            extension = 'rtf'
        else:
            raise ValueError("Unsupported report format")

        full_filename = os.path.join(self.report_dir, f"{filename}.{extension}")

        with open(full_filename, 'w', encoding='utf-8') as f:
            f.write(report.result)

    def test_generate_reports_using_factory(self):
        data_mapping = {
            'group': self.reposity.group_key(),
            'range': self.reposity.range_key(),
            'nomenclature': self.reposity.nomenclature_key(),
            'recipes': self.reposity.recipes_key()
        }

        for report_name, data_key in data_mapping.items():
            data = self.reposity.data[data_key]
            
            for report_format in [format_reporting.CSV, format_reporting.MARKDOWN, format_reporting.JSON, format_reporting.XML, format_reporting.RTF]:
                
                report = report_factory(self.manager).create(report_format)
                report.create(data)
                self._save_report_to_file(report, f'{report_name}_report')

class test_json_report_deserializer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report_dir = os.path.join(os.path.dirname(__file__), 'reports')
        if not os.path.exists(cls.report_dir):
            os.makedirs(cls.report_dir)

        cls.manager = settings_manager()
        cls.rec_manager = recipe_manager()
        cls.reposity = data_reposity()
        cls.start = start_service(cls.reposity, cls.manager, cls.rec_manager)
        cls.start.create()
    def test_json_deserializer(self):
        for file_name in os.listdir("tests/reports"):
            if file_name.endswith('.json'):
                with open(os.path.join("tests/reports", file_name), 'r', encoding="utf-8") as f:
                    json_data = f.read()

                models = json_deserializer.deserialize_json(json_data)

                for model_instance in models:
                    model_name = model_instance.__class__.__name__

                    print(f"Файл {file_name} содержит модель: {model_instance}")

                    self.assertIsNotNone(model_name, "Название модели не должно быть пустым")
    
    def test_serialization_deserialization(self):
        data_mapping = {
            'group': self.reposity.group_key(),
            'range': self.reposity.range_key(),
            'nomenclature': self.reposity.nomenclature_key(),
            'recipes': self.reposity.recipes_key()
        }

        for report_name, data_key in data_mapping.items():
            data = self.reposity.data[data_key]
            
            report = report_factory(self.manager).create(format_reporting.JSON)
            report.create(data)
            json_data = report.result

            deserialized_models = json_deserializer.deserialize_json(json_data)
            
            for original_model, deserialized_model in zip(data, deserialized_models):
                # assert original_model == deserialized_model
                self.assertEqual(original_model, deserialized_model, 
                                 f"Оригинальный объект {original_model} не равен десериализованному объекту {deserialized_model}")