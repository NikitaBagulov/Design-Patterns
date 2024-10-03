import connexion
app = connexion.FlaskApp(__name__)

@app.route("/api/reports/formats", methods=["GET"])
def formats():
    return [{"name":"CSV", "value": 1}]

if __name__ == '__main__':
    # app.add_api("swagger.yaml")
    app.run(port = 8080)