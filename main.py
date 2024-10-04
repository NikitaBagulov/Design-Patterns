import connexion
from flask import jsonify
from src.core.format_reporting import format_reporting
from src.data_reposity import data_reposity
from src.reports.report_factory import report_factory
from src.settings_manager import settings_manager
from src.start_service import start_service
from src.utils.recipe_manager import recipe_manager

app = connexion.FlaskApp(__name__)

@app.route("/api/reports/formats", methods=["GET"])
def formats():
    return [{"name":item.name, "value": item.value} for item in format_reporting]

@app.route("/api/reports/<category>/<format_type>", methods=["GET"])
def get_report(category, format_type):
    manager = settings_manager()
    reposity = data_reposity()
    rec_manager = recipe_manager()
    start = start_service(reposity, manager, rec_manager)
    start.create()

    data_mapping = {
        'range': reposity.range_key(),
        'group': reposity.group_key(),
        'nomenclature': reposity.nomenclature_key(),
        'recipes': reposity.recipes_key()
    }

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

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port = 8080)