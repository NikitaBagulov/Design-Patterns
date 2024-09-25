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
from src.reports.csv_report import csv_report
from src.utils.custom_exceptions import ArgumentException

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
       
        # Действие
        report = report_factory().create( format_reporting.CSV )

        # Проверка
        assert report is not None
        assert isinstance(report,  csv_report)

    def test_report_factory_create_fail(self):
        manager = settings_manager()
        rec_manager = recipe_manager()
        reposity = data_reposity()
        start = start_service(reposity, manager, rec_manager)
        start.create()        
        factory = report_factory()
       
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
                report = report_factory().create(report_format)
                report.create(data)
                self._save_report_to_file(report, f'{report_name}_report.{str(report_format).lower()}')