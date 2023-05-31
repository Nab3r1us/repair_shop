from flask import Blueprint, current_app, jsonify, request, make_response
import os
import sys
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)
from models import db, Schedule

schedules_blueprint = Blueprint("schedules_blueprint", __name__)


@schedules_blueprint.route("/schedules", methods=["POST"])
def create_schedule():
    """
    Создание задачи в расписание
    ---
    tags:
        - Schedule
    produces:
        - application/json
    parameters:
        - in: body
          name: JSON
          required: True
          example: {
              date: 01.04.2023,
              employee_id: 1,
              order_id: 1
          }
    responses:
        201:
            description: '{ "message": "schedule created" }'
    """
    try:
        data = request.get_json()
        new_schedule = Schedule(
            date=data["date"],
            employee_id=data["employee_id"],
            order_id=data["order_id"],
        )
        db.session.add(new_schedule)
        db.session.commit()
        return make_response(jsonify({"message": "schedule created"}), 201)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error creating schedule"}), 500)


@schedules_blueprint.route("/schedules", methods=["GET"])
def get_schedules():
    """
    Получение всех задач в расписании
    ---
    tags:
        - Schedule
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        schedules = Schedule.query.all()
        return make_response(jsonify([schedule.json() for schedule in schedules]), 200)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error getting schedules"}), 500)


@schedules_blueprint.route("/schedules/<int:id>", methods=["GET"])
def get_schedule(id):
    """
    Получение конкретной задачи в расписании
    ---
    tags:
        - Schedule
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
        schedule = Schedule.query.filter_by(id=id).first()
        if schedule:
            return make_response(jsonify({"schedule": schedule.json()}), 200)
        return make_response(jsonify({"message": "schedule not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error getting schedule"}), 500)


@schedules_blueprint.route("/schedules/<int:id>", methods=["PUT"])
def update_schedule(id):
    """
    Редактирование конкретной задачи в расписании
    ---
    tags:
        - Schedule
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
              date: 02.04.2023,
              employee_id: 1,
              order_id: 1
          }
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        schedule = Schedule.query.filter_by(id=id).first()
        if schedule:
            data = request.get_json()
            schedule.date = data["date"]
            schedule.employee_id = data["employee_id"]
            schedule.order_id = data["order_id"]
            db.session.commit()
            return make_response(jsonify({"message": "schedule updated"}), 200)
        return make_response(jsonify({"message": "schedule not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error updating schedule"}), 500)


@schedules_blueprint.route("/schedules/<int:id>", methods=["DELETE"])
def delete_schedule(id):
    """
    Удаление конкретной задачи в расписании
    ---
    tags:
        - Schedule
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
        schedule = Schedule.query.filter_by(id=id).first()
        if schedule:
            db.session.delete(schedule)
            db.session.commit()
            return make_response(jsonify({"message": "schedule deleted"}), 200)
        return make_response(jsonify({"message": "schedule not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error deleting schedule"}), 500)
