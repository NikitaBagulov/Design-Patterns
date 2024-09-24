from src.start_service import start_service
from src.settings_manager import settings_manager
from src.utils.recipe_manager import recipe_manager
from src.data_reposity import data_reposity
from src.reports.csv_report import csv_report
from src.reports.markdown_report import markdown_report
from src.reports.report_factory import report_factory
from src.core.format_reporting import format_reporting
from src.reports.csv_report import csv_report

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

    # """
    # Проверить работу фабрики. Не реализован формат
    # """
    # def test_report_factory_create_fail(self):
    #     manager = settings_manager()
    #     rec_manager = recipe_manager()
    #     reposity = data_reposity()
    #     start = start_service(reposity, manager, rec_manager)
    #     start.create()        
    #     factory = report_factory()
       
    #     # Действие
    #     report = factory.create( format_reporting.MARKDOWN )

    #     # Проверка
    #     assert report is None
    #     assert factory.is_error == True