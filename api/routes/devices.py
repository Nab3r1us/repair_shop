from flask import Blueprint, current_app, jsonify, request, make_response
import os
import sys
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)
from models import db, Devices

devices_blueprint = Blueprint("devices_blueprint", __name__)


@devices_blueprint.route("/devices", methods=["POST"])
def create_device():
    """
    Создание устройства
    ---
    tags:
        - Devices
    produces:
        - application/json
    parameters:
        - in: body
          name: JSON
          required: True
          example: {
              manufacturer: HP,
              model: 620,
              sn: CSD8762SDF,
              release_date: "01.10.2010",
              purchase_date: "03.12.2010",
              client_id: 1
          }
    responses:
        201:
            description: '{ "message": "device created" }'
    """
    try:
        data = request.get_json()
        new_device = Devices(
            manufacturer=data["manufacturer"],
            model=data["model"],
            sn=data["sn"],
            release_date=data["release_date"],
            purchase_date=data["purchase_date"],
            client_id=data["client_id"],
        )
        db.session.add(new_device)
        db.session.commit()
        return make_response(jsonify({"message": "device created"}), 201)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error creating device"}), 500)


@devices_blueprint.route("/devices", methods=["GET"])
def get_devices():
    """
    Получение всех устройств
    ---
    tags:
        - Devices
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        devices = Devices.query.all()
        return make_response(jsonify([device.json() for device in devices]), 200)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error getting devices"}), 500)


@devices_blueprint.route("/devices/<int:id>", methods=["GET"])
def get_device(id):
    """
    Получение конкретного устройства
    ---
    tags:
        - Devices
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
        device = Devices.query.filter_by(id=id).first()
        if device:
            return make_response(jsonify({"device": device.json()}), 200)
        return make_response(jsonify({"message": "device not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error getting device"}), 500)


@devices_blueprint.route("/devices/<int:id>", methods=["PUT"])
def update_device(id):
    """
    Редактирование конкретного устройства
    ---
    tags:
        - Devices
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
              manufacturer: HP,
              model: 620,
              sn: DFS325FDS,
              release_date: 01.10.2010,
              purchase_date: 03.12.2010,
              client_id: 1
          }
    responses:
        200:
            description: Пример успешного ответа
    """
    try:
        device = Devices.query.filter_by(id=id).first()
        if device:
            data = request.get_json()
            device.manufacturer = data["manufacturer"]
            device.model = data["model"]
            device.sn = data["sn"]
            device.release_date = data["release_date"]
            device.purchase_date = data["purchase_date"]
            device.client_id = data["client_id"]
            db.session.commit()
            return make_response(jsonify({"message": "device updated"}), 200)
        return make_response(jsonify({"message": "device not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error updating device"}), 500)


@devices_blueprint.route("/devices/<int:id>", methods=["DELETE"])
def delete_device(id):
    """
    Удаление конкретного устройства
    ---
    tags:
        - Devices
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
        device = Devices.query.filter_by(id=id).first()
        if device:
            db.session.delete(device)
            db.session.commit()
            return make_response(jsonify({"message": "device deleted"}), 200)
        return make_response(jsonify({"message": "device not found"}), 404)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify({"message": "error deleting device"}), 500)
