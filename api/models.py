import enum
from database import db


class Clients(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
        }


class Devices(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(255), unique=True, nullable=False)
    model = db.Column(db.String(255), unique=True, nullable=False)
    sn = db.Column(db.String(255), unique=True, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    client_id = db.Column(db.Integer, unique=True, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "sn": self.sn,
            "release_date": self.release_date,
            "purchase_date": self.purchase_date,
            "client_id": self.client_id,
        }


class Employees(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    surname = db.Column(db.String(255), unique=True, nullable=False)
    post = db.Column(db.String(255), unique=True, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "post": self.post,
        }


class Orders(db.Model):
    __tablename__ = "orders"

    class States(enum.Enum):
        pending = "ожидание"
        in_progress = "в работе"
        completed = "завершен"

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, unique=True, nullable=False)
    device_id = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(255), unique=True, nullable=False)
    cost = db.Column(db.Float, unique=True, nullable=False)
    state = db.Column(db.Enum(States), unique=True, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "order_date": self.order_date,
            "device_id": self.device_id,
            "description": self.description,
            "cost": self.cost,
            "state": self.state.value,
        }


class Payments(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    payment_date = db.Column(db.DateTime, unique=True, nullable=False)
    order_id = db.Column(db.Integer, unique=True, nullable=False)
    amount = db.Column(db.Float, unique=True, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "payment_date": self.payment_date,
            "order_id": self.order_id,
            "amount": self.amount,
        }


class Schedule(db.Model):
    __tablename__ = "schedule"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True, nullable=False)
    employee_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, unique=True, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "date": self.date,
            "employee_id": self.employee_id,
            "order_id": self.order_id,
        }
