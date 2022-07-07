import string

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask import json
import datetime

db = SQLAlchemy()


class Aggregate:
    @classmethod
    def convert_date(cls, data: dict) -> dict:
        data_changed = {}
        for key, data in data.items():
            if 'date' in key:
                month, day, year = data.split('/')
                date_new = datetime.date(int(year), int(month), int(day))
                data_changed[key] = date_new
            else:
                data_changed[key] = data
        return data_changed

    @classmethod
    def create_database(cls, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data_to_be_added = []
        for item in data:
            new_item = cls.convert_date(item)
            data_to_be_added.append(cls(**new_item))
        print(data_to_be_added)
        return data_to_be_added


class User(db.Model, Aggregate):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    orders = relationship('Order', backref='orders')

    def __repr__(self) -> str:
        return f"Line {self.id} from json file was created"

    def instance_to_dict(self):
        return {
                'id'        : self.id,
                'first_name': self.first_name,
                'last_name' : self.last_name,
                'age'       : self.age,
                'email'     : self.email,
                'role'      : self.role,
                'phone'     : self.phone
        }


class Order(db.Model, Aggregate):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer)

    user = relationship('User', backref='user')

    def __repr__(self):
        return f"Line {self.id} from json file was created"

    def instance_to_dict(self):
        return {
                'id'         : self.id,
                'name'       : self.name,
                'description': self.description,
                'start_date' : self.start_date,
                'end_date'   : self.end_date,
                'address'    : self.address,
                'price'      : self.price,
                'customer_id': self.customer_id,
                'executor_id': self.executor_id
        }


class Offer(db.Model, Aggregate):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'Line {self.id} from json file was created'

    def instance_to_dict(self):
        return {
                'id'         : self.id,
                'order_id'   : self.order_id,
                'executor_id': self.executor_id
        }
