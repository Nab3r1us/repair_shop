from flask import Blueprint, current_app, jsonify, request, make_response
import os
import sys
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)
from models import db, Payments

payments_blueprint = Blueprint("payments_blueprint", __name__)


@payments_blueprint.route("/payments", methods=["POST"])
def create_payment():
    """
    Создание платежа
    ---
    tags:
        - Payments
    produces:
        - application/json
    parameters:
        - in: body
          name: JSON
          required: True
          example: {
              payment_date: 02.04.2023,
              order_id: 1,
              amount: 99.99
          }
    responses:
        201:
            description: '{ "message": "payment created" }'
    """
    try:
        data = request.get_json()
        new_payment = Payments(
            payment_date=data["payment_date"],
            order_id=data["order_id"],
            amount=data["amount"],
        )
        db.session.add(new_payment)
        db.session.commit()
        return make_response(jsonify({"message": "payment created"}), 201)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error creating payment"}), 500)


@payments_blueprint.route("/payments", methods=["GET"])
def get_payments():
    """
    Получение всех платежей
    ---
    tags:
        - Payments
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        payments = Payments.query.all()
        return make_response(jsonify([payment.json() for payment in payments]), 200)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error getting payments"}), 500)


@payments_blueprint.route("/payments/<int:id>", methods=["GET"])
def get_payment(id):
    """
    Получение конкретного платежа
    ---
    tags:
        - Payments
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
        payment = Payments.query.filter_by(id=id).first()
        if payment:
            return make_response(jsonify({"payment": payment.json()}), 200)
        return make_response(jsonify({"message": "payment not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error getting payment"}), 500)


@payments_blueprint.route("/payments/<int:id>", methods=["PUT"])
def update_payment(id):
    """
    Редактирование конкретного платежа
    ---
    tags:
        - Payments
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
              payment_date: 02.04.2023,
              order_id: 1,
              amount: 89.99
          }
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        payment = Payments.query.filter_by(id=id).first()
        if payment:
            data = request.get_json()
            payment.payment_date = data["payment_date"]
            payment.order_id = data["order_id"]
            payment.amount = data["amount"]
            db.session.commit()
            return make_response(jsonify({"message": "payment updated"}), 200)
        return make_response(jsonify({"message": "payment not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error updating payment"}), 500)


@payments_blueprint.route("/payments/<int:id>", methods=["DELETE"])
def delete_payment(id):
    """
    Удаление конкретного платежа
    ---
    tags:
        - Payments
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
        payment = Payments.query.filter_by(id=id).first()
        if payment:
            db.session.delete(payment)
            db.session.commit()
            return make_response(jsonify({"message": "payment deleted"}), 200)
        return make_response(jsonify({"message": "payment not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error deleting payment"}), 500)
