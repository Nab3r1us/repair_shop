from flask import Flask
from routes import routes_blueprint
from database import init_db, create_all
from swagger import swagger_blueprint, swaggerui_blueprint, init_swagger
from os import environ


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
init_db(app)
app.register_blueprint(routes_blueprint)
init_swagger(app)
app.register_blueprint(swaggerui_blueprint, url_prefix="/swagger")
app.register_blueprint(swagger_blueprint)


if __name__ == '__main__':
    with app.app_context():
        create_all()
    app.run(debug=True, host="0.0.0.0")
