import connexion
from flask import jsonify, request
from src.core.format_reporting import format_reporting
from src.data_reposity import data_reposity
from src.reports.report_factory import report_factory
from src.settings_manager import settings_manager
from src.start_service import start_service
from src.utils.recipe_manager import recipe_manager
from src.logics.domain_prototype import domain_prototype
from src.logics.warehouse_transaction_prototype import warehouse_transaction_prototype
from src.dto.filter_dto import filter_dto, warehouse_nomenclature_filter_dto
from datetime import datetime
from src.processors.process_factory import process_factory
from src.processors.warehouse_turnover_process import warehouse_turnover_process

app = connexion.FlaskApp(__name__)
manager = settings_manager()
reposity = data_reposity()
rec_manager = recipe_manager()
start = start_service(reposity, manager, rec_manager)
start.create()

data_mapping = reposity.keys()

@app.route("/api/reports/formats", methods=["GET"])
def formats():
    return [{"name":item.name, "value": item.value} for item in format_reporting]

@app.route("/api/reports/<category>/<format_type>", methods=["GET"])
def get_report(category, format_type):

    if category not in data_mapping:
        return jsonify({"error": "Invalid category"}), 400

    try:
        report_format = format_reporting[format_type.upper()]
    except KeyError:
        return jsonify({"error": "Invalid report format"}), 400

    data = reposity.data[data_mapping[category]]
    report = report_factory(manager).create(report_format)
    report.create(data)

    return report.result, 200

@app.route("/api/filter/<domain_type>", methods=["POST"])
def filter_data(domain_type):
    if domain_type not in data_mapping:
        return jsonify({"error": "Invalid domain type"}), 400

    filter_data = request.get_json()
    try:
        filt = filter_dto.create(filter_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    data = reposity.data[data_mapping[domain_type]]
    if not data:
        return jsonify({"error": "No data available"}), 404
    prototype = domain_prototype(data)
    filtered_data = prototype.create(data, filt)
    if not filtered_data.data:
        return jsonify({"message": "No data found"}), 404
        
    report = report_factory(manager).create(format_reporting.JSON)
    report.create(filtered_data.data)
    return report.result

@app.route("/api/filter/transactions", methods=["POST"])
def get_transactions():
    filter_data = request.get_json()

    filt = warehouse_nomenclature_filter_dto.create(filter_data)
    data = reposity.data[data_mapping[data_reposity.transactions_key()]]
    if not data:
        return jsonify({"error": "No data available"}), 404

    prototype = warehouse_transaction_prototype(data)

    filtered_data = prototype.create(data, filt)


    if not filtered_data.data:
        return jsonify({"message": "No transactions found"}), 404

    report = report_factory(manager).create(format_reporting.JSON)
    report.create(filtered_data.data)
    return report.result

@app.route("/api/filter/turnover", methods=["POST"])
def get_turnover():
    try:
        filter_data = request.get_json()
        warehouse_filt = warehouse_nomenclature_filter_dto.create(filter_data)
        data = reposity.data[data_mapping[data_reposity.transactions_key()]]
        if not data:
            return jsonify({"error": "No data available"}), 404

        prototype = warehouse_transaction_prototype(data)
        filtered_data = prototype.create(data, warehouse_filt)


        if not filtered_data.data:
            return jsonify({"message": "No transactions found"}), 404

        factory = process_factory()
        factory.register_process('turnover', warehouse_turnover_process)
        process = factory.get_process('turnover')
        turnovers = process.process(filtered_data.data)

        if not turnovers:
            return jsonify({"message": "No turnovers found"}), 404

        report = report_factory(manager).create(format_reporting.JSON)
        report.create(turnovers)

        return report.result
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port = 8080)