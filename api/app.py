from flask import Flask
from routes.clients import clients_blueprint
from routes.devices import devices_blueprint
from routes.orders import orders_blueprint
from routes.payments import payments_blueprint
from routes.employees import employees_blueprint
from routes.schedules import schedules_blueprint
from database import init_db, create_all
from swagger import swagger_blueprint, swaggerui_blueprint, init_swagger
from os import environ


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
init_db(app)
app.register_blueprint(clients_blueprint)
app.register_blueprint(devices_blueprint)
app.register_blueprint(orders_blueprint)
app.register_blueprint(payments_blueprint)
app.register_blueprint(employees_blueprint)
app.register_blueprint(schedules_blueprint)
init_swagger(app)
app.register_blueprint(swaggerui_blueprint, url_prefix="/swagger")
app.register_blueprint(swagger_blueprint)


if __name__ == '__main__':
    with app.app_context():
        create_all()
    app.run(debug=True, host="0.0.0.0")
