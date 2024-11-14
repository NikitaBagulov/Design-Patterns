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
from src.logics.nomenclature_service import nomenclature_service
from src.processors.process_factory import process_factory
from src.processors.warehouse_turnover_process import warehouse_turnover_process
from src.models.nomenclature import nomenclature_model

from src.logics.observe_service import observe_service
from src.core.event_type import event_type

from src.reports.turnover_balance_sheet import turnover_balance_sheet
from src.reposity_manager import reposity_manager


app = connexion.FlaskApp(__name__)
manager = settings_manager()
reposity = data_reposity()
reposity_manager = reposity_manager(reposity, manager)
rec_manager = recipe_manager()
start = start_service(reposity, manager, rec_manager)
nomenclature_service_instance = nomenclature_service(reposity)
balance_sheet = turnover_balance_sheet(reposity)


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

@app.route('/api/settings/block_period', methods=['POST'])
def set_block_period():
    data = request.get_json()
    block_period_str = data.get('block_period')

    try:

        settings = manager.settings 
        settings.block_period = block_period_str
        observe_service.raise_event( event_type.CHANGE_BLOCK_PERIOD , None)
        return jsonify({"message": "Дата блокировки обновлена успешно."}), 200
    except (ValueError, AttributeError) as e:
        return jsonify({"error": "Неправильный формат даты или ошибка запроса.", "details": str(e)}), 400

@app.route('/settings/block_period', methods=['GET'])
def get_block_period():
    settings = manager.settings
    block_period_str = settings.block_period.strftime("%Y-%m-%d") if settings.block_period else None
    return jsonify({"block_period": block_period_str}), 200

@app.route('/api/nomenclature', methods=['GET'])
def get_nomenclature():
    result = nomenclature_service_instance.get_nomenclature(request.args)
    if "error" in result or "status" in result:
        return jsonify(result), 404 if "error" in result else 200
    
    report = report_factory(manager).create(format_reporting.JSON)
    report.create(list(result))
    return report.result, 200

@app.route('/api/nomenclature', methods=['PUT'])
def add_nomenclature():
    result = nomenclature_service_instance.add_nomenclature(request.json)
    if not isinstance(result, nomenclature_model):
        return jsonify(result), 400

    report = report_factory(manager).create(format_reporting.JSON)
    report.create([result])
    observe_service.raise_event(event_type.CREATE_OSV, {})
    return report.result, 201


@app.route('/api/nomenclature', methods=['PATCH'])
def update_nomenclature():
    statuses = observe_service.raise_event(event_type.CHANGE_NOMENCLATURE, request.json)
    status = statuses[type(nomenclature_service_instance).__name__]
    observe_service.raise_event(event_type.CREATE_OSV, {})
    return jsonify(status), 200

@app.route('/api/nomenclature', methods=['DELETE'])
def delete_nomenclature():
    try:
        statuses = observe_service.raise_event(event_type.DELETE_NOMENCLATURE, request.json)
        status = statuses[type(nomenclature_service_instance).__name__]
        observe_service.raise_event(event_type.CREATE_OSV, {})
        return jsonify(status), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/report/osv", methods=["GET"])
def get_osv_report():
    try:
        start_date_str = request.args.get("start_date")
        end_date_str = request.args.get("end_date")
        warehouse = request.args.get("warehouse")

        if not start_date_str or not end_date_str or not warehouse:
            return jsonify({"error": "Отсутствуют обязательные параметры: 'start_date', 'end_date', or 'warehouse'"}), 400
        balance_sheet.start_date = start_date_str
        balance_sheet.end_date = end_date_str
        balance_sheet.warehouse = warehouse
        statuses = observe_service.raise_event(event_type.CREATE_OSV, {})
        status = statuses[type(balance_sheet).__name__]
        return jsonify(status), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/api/repository/save", methods=["POST"])
def save_repository():
    try:
        observe_service.raise_event(event_type.SAVE_REPOSITY,{})
        return jsonify({"message": "Данные успешно сохранены в файл."}), 200
    except Exception as e:
        return jsonify({"error": f"Ошибка при сохранении данных в файл: {str(e)}"}), 500

@app.route("/api/repository/restore", methods=["POST"])
def restore_repository():
    try:
        observe_service.raise_event(event_type.LOAD_REPOSITY, {})
        return jsonify({"message": "Данные успешно восстановлены из файла."}), 200
    except Exception as e:
        return jsonify({"error": f"Ошибка при восстановлении данных из файла: {str(e)}"}), 500

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port = 8080)