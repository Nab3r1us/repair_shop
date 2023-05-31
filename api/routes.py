from flask import Blueprint, current_app, jsonify, request, make_response
from models import db, Clients, Devices, Employees, Orders, Payments, Schedule

routes_blueprint = Blueprint("routes_blueprint", __name__)

@routes_blueprint.route("/clients", methods=["POST"])
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


@routes_blueprint.route("/clients", methods=["GET"])
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


@routes_blueprint.route("/clients/<int:id>", methods=["GET"])
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


@routes_blueprint.route("/clients/<int:id>", methods=["PUT"])
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


@routes_blueprint.route("/clients/<int:id>", methods=["DELETE"])
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



@routes_blueprint.route("/devices", methods=["POST"])
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


@routes_blueprint.route("/devices", methods=["GET"])
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


@routes_blueprint.route("/devices/<int:id>", methods=["GET"])
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


@routes_blueprint.route("/devices/<int:id>", methods=["PUT"])
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


@routes_blueprint.route("/devices/<int:id>", methods=["DELETE"])
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


@routes_blueprint.route("/orders", methods=["POST"])
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


@routes_blueprint.route("/orders", methods=["GET"])
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


@routes_blueprint.route("/orders/<int:id>", methods=["GET"])
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


@routes_blueprint.route("/orders/<int:id>", methods=["PUT"])
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


@routes_blueprint.route("/orders/<int:id>", methods=["DELETE"])
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



@routes_blueprint.route("/payments", methods=["POST"])
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


@routes_blueprint.route("/payments", methods=["GET"])
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


@routes_blueprint.route("/payments/<int:id>", methods=["GET"])
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


@routes_blueprint.route("/payments/<int:id>", methods=["PUT"])
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


@routes_blueprint.route("/payments/<int:id>", methods=["DELETE"])
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



@routes_blueprint.route("/employees", methods=["POST"])
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


@routes_blueprint.route("/employees", methods=["GET"])
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


@routes_blueprint.route("/employees/<int:id>", methods=["GET"])
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


@routes_blueprint.route("/employees/<int:id>", methods=["PUT"])
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


@routes_blueprint.route("/employees/<int:id>", methods=["DELETE"])
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



@routes_blueprint.route("/schedules", methods=["POST"])
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


@routes_blueprint.route("/schedules", methods=["GET"])
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


@routes_blueprint.route("/schedules/<int:id>", methods=["GET"])
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


@routes_blueprint.route("/schedules/<int:id>", methods=["PUT"])
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


@routes_blueprint.route("/schedules/<int:id>", methods=["DELETE"])
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

