from model import db, User, Order, Offer
from view import app
from flask import request, jsonify, redirect

"""
Сервисный слой бизнес-логики
"""


def fill_databases():
    """заполнение инстантами БД"""
    with db.session.begin():
        users = User.create_database(app.config.get('USERS'))
        orders = Order.create_database(app.config.get('ORDERS'))
        offers = Offer.create_database(app.config.get('OFFERS'))
        db.session.add_all(users)
        db.session.add_all(orders)
        db.session.add_all(offers)


def drop_databases():
    """сброс таблиц БД"""
    db.drop_all()


def create_database():
    """создание БД по коммиту"""
    db.create_all()


def users_all(method: str = "GET"):
    """Отработка вызова эндпоинта дефолтный метод ГЕТ"""
    if method == 'POST':
        with db.session.begin():
            user = User(**request.json)
            db.session.add(user)
        return jsonify(user.instance_to_dict())
    else:
        users = User.query.all()
        users_json = [user.instance_to_dict() for user in users]
        return jsonify(users_json)


def users_id(idx: int, method: str = "GET"):
    """Отработка вызова эндпоинта дефолтный метод ГЕТ"""
    if method == 'PUT':
        data = request.json
        with db.session.begin():
            user = User.query.filter(User.id == idx).one()
            user.update(data)
        return jsonify(user.instance_to_dict())
    elif method == 'DELETE':
        with db.session.begin():
            User.query.filter(User.id == idx).delete()
        return redirect('/users', 302)
    else:
        user = User.query.filter(User.id == idx).one()
        return jsonify(user.instance_to_dict())


def orders_all(method: str = "GET"):
    """Отработка вызова эндпоинта дефолтный метод ГЕТ"""
    if method == 'POST':
        with db.session.begin():
            data = request.json
            data_changed = Order.convert_date(data)
            order = Order(**data_changed)
            db.session.add(order)
        return jsonify(order.instance_to_dict())
    else:
        orders = Order.query.all()
        orders_json = [order.instance_to_dict() for order in orders]
        return jsonify(orders_json)


def orders_by_id(idx, method: str = "GET"):
    """Отработка вызова эндпоинта дефолтный метод ГЕТ"""
    if method == 'PUT':
        data = request.json
        data_changed = Order.convert_date(data)
        with db.session.begin():
            order = Order.query.filter(Order.id == idx).one()
            order.update(data_changed)
        return jsonify(order.instance_to_dict())

    elif method == 'DELETE':
        with db.session.begin():
            Order.query.filter(Order.id == idx).delete()
        return redirect('/orders', 302)

    else:
        order = Order.query.filter(Order.id == idx).one()
        return jsonify(order.instance_to_dict())


def offers_all(method: str = "GET"):
    """Отработка вызова эндпоинта дефолтный метод ГЕТ"""
    if method == 'POST':
        with db.session.begin():
            offer = Offer(**request.json)
            db.session.add(offer)
        return jsonify(offer.instance_to_dict())
    else:
        offers = Offer.query.all()
        offers_json = [offer.instance_to_dict() for offer in offers]
        return jsonify(offers_json)


def offers_by_id(idx, method: str = "GET"):
    """Отработка вызова эндпоинта дефолтный метод ГЕТ"""
    if method == 'PUT':
        data = request.json
        with db.session.begin():
            offer = Offer.query.filter(Offer.id == idx).one()
            offer.update(data)
        return jsonify(offer.instance_to_dict())

    elif method == 'DELETE':
        with db.session.begin():
            Offer.query.filter(Order.id == idx).delete()
        return redirect('/offers', 302)

    else:
        offer = Offer.query.filter(Offer.id == idx).one()
        return jsonify(offer.instance_to_dict())
