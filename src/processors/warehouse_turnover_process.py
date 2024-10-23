from datetime import datetime
from src.logics.warehouse_turnover_prototype import warehouse_turnover_prototype
from src.core.abstract_process import abstract_process

class warehouse_turnover_process(abstract_process):

    def process(self, transactions, warehouse=None, nomenclature=None, start_period=None, end_period=None) -> list:
        turnovers = {}

        for transaction in transactions:
            if start_period and not (start_period <= transaction.period <= end_period):
                continue
            if warehouse and transaction.warehouse.name != warehouse:
                continue
            if nomenclature and transaction.nomenclature.name != nomenclature:
                continue

            key = (transaction.warehouse.unique_code, transaction.nomenclature.unique_code, transaction.range.unique_code)

            if key not in turnovers:
                turnovers[key] = warehouse_turnover_prototype(
                    warehouse=transaction.warehouse,
                    nomenclature=transaction.nomenclature,
                    range=transaction.range
                )

            if transaction.is_incoming:
                turnovers[key].turnover += transaction.quantity
            else:
                turnovers[key].turnover -= transaction.quantity

        return list(turnovers.values())