from flask import Blueprint, current_app, jsonify, request, make_response
import os
import sys
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)
from models import db, Employees

employees_blueprint = Blueprint("employees_blueprint", __name__)


@employees_blueprint.route("/employees", methods=["POST"])
def create_employee():
    """
    Создание сотрудника
    ---
    tags:
        - Employees
    produces:
        - application/json
    parameters:
        - in: body
          name: JSON
          required: True
          example: {
              name: Иван,
              surname: Иванов,
              post: Мастер
          }
    responses:
        201:
            description: '{ "message": "employee created" }'
    """
    try:
        data = request.get_json()
        new_employee = Employees(
            name=data["name"],
            surname=data["surname"],
            post=data["post"],
        )
        db.session.add(new_employee)
        db.session.commit()
        return make_response(jsonify({"message": "employee created"}), 201)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error creating employee"}), 500)


@employees_blueprint.route("/employees", methods=["GET"])
def get_employees():
    """
    Получение всех сотрудников
    ---
    tags:
        - Employees
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        employees = Employees.query.all()
        return make_response(jsonify([employee.json() for employee in employees]), 200)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error getting employees"}), 500)


@employees_blueprint.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):
    """
    Получение конкретного сотрудника
    ---
    tags:
        - Employees
    parameters:
        - in: path
          name: id
          type: integer
          example: 1
          required: True
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        employee = Employees.query.filter_by(id=id).first()
        if employee:
            return make_response(jsonify({"employee": employee.json()}), 200)
        return make_response(jsonify({"message": "employee not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error getting employee"}), 500)


@employees_blueprint.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):
    """
    Редактирование конкретного сотрудника
    ---
    tags:
        - Employees
    produces:
        - application/json
    parameters:
        - in: path
          name: id
          type: integer
          example: 1
          required: True
        - in: body
          name: JSON
          required: True
          example: {
              name: Иван,
              surname: Иванов,
              post: Старший мастер
          }
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        employee = Employees.query.filter_by(id=id).first()
        if employee:
            data = request.get_json()
            employee.name = data["name"]
            employee.surname = data["surname"]
            employee.post = data["post"]
            db.session.commit()
            return make_response(jsonify({"message": "employee updated"}), 200)
        return make_response(jsonify({"message": "employee not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error updating employee"}), 500)


@employees_blueprint.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    """
    Удаление конкретного сотрудника
    ---
    tags:
        - Employees
    parameters:
        - in: path
          name: id
          type: integer
          example: 1
          required: True
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        employee = Employees.query.filter_by(id=id).first()
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return make_response(jsonify({"message": "employee deleted"}), 200)
        return make_response(jsonify({"message": "employee not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error deleting employee"}), 500)
