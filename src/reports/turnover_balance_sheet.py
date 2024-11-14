from datetime import datetime
from src.core.event_type import event_type
from src.core.abstract_logic import abstract_logic
from src.data_reposity import data_reposity
from src.logics.observe_service import observe_service
from src.utils.validator import Validator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

class turnover_balance_sheet(abstract_logic):
    __start_date: datetime
    __end_date: datetime
    __warehouse: str 

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value: str):
        Validator.validate_type(value, str, "start_date")
        self.__start_date = datetime.strptime(value, "%Y-%m-%d") 

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, value: str):
        Validator.validate_type(value, str, "end_date")
        self.__end_date = datetime.strptime(value, "%Y-%m-%d") 

    @property
    def warehouse(self):
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: str):
        Validator.validate_type(value, str, "warehouse")
        self.__warehouse = value


    def __init__(self, reposity: data_reposity):
        observe_service.append(self)
        self.data = reposity.data.get(reposity.transactions_key())

    def calculate_initial_balance(self):
        initial_balance = {"initial_balance": 0.0, "inflow": 0.0, "outflow": 0.0}
        for transaction in self.data:
            if (transaction.warehouse.name == self.warehouse and 
                transaction.period < self.start_date):
                if transaction.is_incoming:
                    initial_balance["inflow"] += transaction.quantity
                else:
                    initial_balance["outflow"] += transaction.quantity
        initial_balance["initial_balance"] = initial_balance["inflow"] - initial_balance["outflow"]
        return initial_balance

    def calculate_period_transactions(self):
        period_transactions = {"inflow": 0.0, "outflow": 0.0}
        for transaction in self.data:
            if (transaction.warehouse.name == self.warehouse and
                self.start_date <= transaction.period <= self.end_date):
                if transaction.is_incoming:
                    period_transactions["inflow"] += transaction.quantity
                else:
                    period_transactions["outflow"] += transaction.quantity
        return period_transactions

    def calculate_final_balance(self):
        final_balance = {"final_balance": 0.0, "inflow": 0.0, "outflow": 0.0}
        for transaction in self.data:
            if (transaction.warehouse.name == self.warehouse and 
                transaction.period <= self.end_date):
                if transaction.is_incoming:
                    final_balance["inflow"] += transaction.quantity
                else:
                    final_balance["outflow"] += transaction.quantity
        final_balance["final_balance"] = final_balance["inflow"] - final_balance["outflow"]
        return final_balance

    def generate_report(self):
        initial_balance = self.calculate_initial_balance()
        period_transactions = self.calculate_period_transactions()
        final_balance = self.calculate_final_balance()

        report = {
            "initial_balance": initial_balance["initial_balance"],
            "inflow": period_transactions["inflow"],
            "outflow": period_transactions["outflow"],
            "final_balance": final_balance["final_balance"],
        }
        report_df = pd.DataFrame(list(report.items()), columns=["Metric", "Amount"])
        self.save_report_as_image(report_df, "turnover_balance_sheet.png")
        return report

    def save_report_as_image(self, df, file_path):
        fig, ax = plt.subplots(figsize=(5, 1))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.5)

        plt.savefig(file_path, bbox_inches='tight', dpi=300)
        
    def set_exception(self, ex: Exception):
        return super().set_exception(ex)

    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)
        if type == event_type.CREATE_OSV:
            return self.generate_report()

