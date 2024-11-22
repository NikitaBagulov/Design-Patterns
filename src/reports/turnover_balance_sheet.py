from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from src.utils.validator import Validator
from src.core.abstract_logic import abstract_logic
from src.logics.observe_service import observe_service
from src.core.event_type import event_type
from src.processors.warehouse_turnover_process import warehouse_turnover_process
from src.settings_manager import settings_manager
from src.core.format_reporting import format_reporting
from src.reports.report_factory import report_factory

import json

class turnover_balance_sheet(abstract_logic):
    _start_date: datetime
    _end_date: datetime
    _warehouse: str = ""

    def __init__(self, data, manager:settings_manager):
        observe_service.append(self)
        self.data = data
        self.manager = manager
        print(self.manager.settings.block_period)

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value: str):
        Validator.validate_type(value, str, "start_date")
        self._start_date = datetime.strptime(value, "%Y-%m-%d") 

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value: str):
        Validator.validate_type(value, str, "end_date")
        self._end_date = datetime.strptime(value, "%Y-%m-%d") 

    @property
    def warehouse(self):
        return self._warehouse

    @warehouse.setter
    def warehouse(self, value: str):
        Validator.validate_type(value, str, "warehouse")
        self._warehouse = value

    def calculate_osv(self, transactions: list, start_date: datetime, end_date: datetime):
        receipt = []
        consumption = []
        opening_turnovers = []
        turnovers = []
        
        process = warehouse_turnover_process(self.manager)
        
        for transaction in transactions:
            if transaction.warehouse.name == self.warehouse:
                if transaction.period <= start_date:
                    opening_turnovers.append(transaction)

                if start_date <= transaction.period <= end_date:
                    turnovers.append(transaction)

                    if transaction.is_incoming:
                        receipt.append(transaction)
                    else:
                        consumption.append(transaction)
        remainder = process.process(turnovers)
        opening_remainder = process.process(opening_turnovers)
        return opening_remainder, receipt, consumption, remainder


    def generate_report(self, request_data):
        self.start_date = request_data.get('start_date')
        self.end_date = request_data.get('end_date')
        self.warehouse = request_data.get('warehouse')

        opening_remainder, receipt, consumption, remainder = self.calculate_osv(self.data, self.start_date, self.end_date)
        report = report_factory(self.manager).create(format_reporting.JSON)
        report_data = {
        "Opening remainders": opening_remainder,
        "Remainders": remainder,
        "Receipts": receipt,
        "Consumptions": consumption,
        }
        for key, result in report_data.items():
            report.create(result)
            report_data[key] = report.result
        with open("osv.json", 'w', encoding='utf-8') as file:
            file.write(json.dumps(report_data))
        return report_data


    def set_exception(self, ex: Exception):
        return super().set_exception(ex)

    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)
        if type == event_type.CREATE_OSV:
            return self.generate_report(params)
