from flask import Blueprint, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

swagger_blueprint = Blueprint("swagger", __name__)


def init_swagger(app):
    global swag
    swag = swagger(app)


@swagger_blueprint.route("/swagger.json")
def get_swagger():
    swag["info"]["version"] = "1.0"
    swag["info"]["title"] = "Repair Shop API"
    swag["tags"] = [
        {"name": "Clients", "description": "API для работы с клиентами"},
        {"name": "Devices", "description": "API для работы с устройствами"},
        {"name": "Employees", "description": "API для работы с сотрудниками"},
        {"name": "Orders", "description": "API для работы с заявками"},
        {"name": "Payments", "description": "API для работы с платежами"},
        {"name": "Schedule", "description": "API для работы с расписанием"},
    ]
    return jsonify(swag)


swaggerui_blueprint = get_swaggerui_blueprint(
    "/swagger",
    "/swagger.json",
    config={
        "app_name": "Repair Shop API"
    }
)
