from flask import Blueprint, current_app, jsonify, request, make_response
import os
import sys
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)
from models import db, Clients

clients_blueprint = Blueprint("clients_blueprint", __name__)


@clients_blueprint.route("/clients", methods=["POST"])
def create_client():
    """
    Создание клиента
    ---
    tags:
        - Clients
    produces:
        - application/json
    parameters:
        - in: body
          name: JSON
          required: True
          example: {
              name: Василий,
              surname: Пупкин,
              address: "г.Витебск, пр-т. Московский 123",
              phone: "+375 33 333-33-33",
              email: vasiliy.pupkin@gmail.com
          }
    responses:
        201:
            description: '{ "message": "client created" }'
    """
    try:
        data = request.get_json()
        new_client = Clients(
            name=data["name"],
            surname=data["surname"],
            address=data["address"],
            phone=data["phone"],
            email=data["email"],
        )
        db.session.add(new_client)
        db.session.commit()
        return make_response(jsonify({"message": "client created"}), 201)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error creating client"}), 500)


@clients_blueprint.route("/clients", methods=["GET"])
def get_clients():
    """
    Получение всех клиентов
    ---
    tags:
        - Clients
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        clients = Clients.query.all()
        return make_response(jsonify([client.json() for client in clients]), 200)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error getting clients"}), 500)


@clients_blueprint.route("/clients/<int:id>", methods=["GET"])
def get_client(id):
    """
    Получение конкретного клиента
    ---
    tags:
        - Clients
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
        client = Clients.query.filter_by(id=id).first()
        if client:
            return make_response(jsonify({"client": client.json()}), 200)
        return make_response(jsonify({"message": "client not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error getting client"}), 500)


@clients_blueprint.route("/clients/<int:id>", methods=["PUT"])
def update_client(id):
    """
    Редактирование конкретного клиента
    ---
    tags:
        - Clients
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
              name: Василий,
              surname: Пупкин,
              address: "г.Витебск, пр-т. Московский 123",
              phone: "+375 33 333-33-33",
              email: vasiliy.pupkin@mail.ru
          }
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        client = Clients.query.filter_by(id=id).first()
        if client:
            data = request.get_json()
            client.name = data["name"] if "name" in data else client.name
            client.surname = data["surname"] if "surname" in data else client.name
            client.address = data["address"] if "address" in data else client.name
            client.phone = data["phone"] if "phone" in data else client.name
            client.email = data["email"] if "email" in data else client.name
            db.session.commit()
            return make_response(jsonify({"message": "client updated"}), 202)
        return make_response(jsonify({"message": "client not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error updating client"}), 500)


@clients_blueprint.route("/clients/<int:id>", methods=["DELETE"])
def delete_client(id):
    """
    Удаление конкретного клиента
    ---
    tags:
        - Clients
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
        client = Clients.query.filter_by(id=id).first()
        if client:
            db.session.delete(client)
            db.session.commit()
            return make_response(jsonify({"message": "client deleted"}), 200)
        return make_response(jsonify({"message": "client not found"}), 204)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error deleting client"}), 500)
