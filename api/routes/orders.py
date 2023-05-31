from flask import Blueprint, current_app, jsonify, request, make_response
import os
import sys
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)
from models import db, Orders

orders_blueprint = Blueprint("orders_blueprint", __name__)


@orders_blueprint.route("/orders", methods=["POST"])
def create_order():
    """
    Создание заявки
    ---
    tags:
        - Orders
    produces:
        - application/json
    parameters:
        - in: body
          name: JSON
          required: True
          example: {
              order_date: 01.04.2023,
              device_id: 1,
              description: "Замена АКБ",
              cost: 70.99,
              state: pending
          }
    responses:
        201:
            description: '{ "message": "order created" }'
    """
    try:
        data = request.get_json()
        new_order = Orders(
            order_date=data["order_date"],
            device_id=data["device_id"],
            description=data["description"],
            cost=data["cost"],
            state=data["state"],
        )
        db.session.add(new_order)
        db.session.commit()
        return make_response(jsonify({"message": "order created"}), 201)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error creating order"}), 500)


@orders_blueprint.route("/orders", methods=["GET"])
def get_orders():
    """
    Получение всех заявок
    ---
    tags:
        - Orders
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        orders = Orders.query.all()
        return make_response(jsonify([order.json() for order in orders]), 200)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error getting orders"}), 500)


@orders_blueprint.route("/orders/<int:id>", methods=["GET"])
def get_order(id):
    """
    Получение конкретной заявки
    ---
    tags:
        - Orders
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
        order = Orders.query.filter_by(id=id).first()
        if order:
            return make_response(jsonify({"order": order.json()}), 200)
        return make_response(jsonify({"message": "order not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error getting order"}), 500)


@orders_blueprint.route("/orders/<int:id>", methods=["PUT"])
def update_order(id):
    """
    Редактирование конкретной заявки
    ---
    tags:
        - Orders
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
              order_date: 01.04.2023,
              device_id: 1,
              description: "Замена АКБ",
              cost: 70.99,
              state: completed
          }
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        order = Orders.query.filter_by(id=id).first()
        if order:
            data = request.get_json()
            order.order_date = data["order_date"]
            order.device_id = data["device_id"]
            order.description = data["description"]
            order.cost = data["cost"]
            order.state = data["state"]
            db.session.commit()
            return make_response(jsonify({"message": "order updated"}), 200)
        return make_response(jsonify({"message": "order not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error updating order"}), 500)


@orders_blueprint.route("/orders/<int:id>", methods=["DELETE"])
def delete_order(id):
    """
    Удаление конкретной заявки
    ---
    tags:
        - Orders
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
        order = Orders.query.filter_by(id=id).first()
        if order:
            db.session.delete(order)
            db.session.commit()
            return make_response(jsonify({"message": "order deleted"}), 200)
        return make_response(jsonify({"message": "order not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error deleting order"}), 500)
