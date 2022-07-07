from flask import Flask, jsonify, render_template, request, redirect
from model import db, User, Order, Offer

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


@app.route('/')
def index(): return render_template('index.html')


# Основной аггрегатор БД - создание таблиц, удаление таблиц, наполнение данными
@app.route('/add')
def db_index():
    with db.session.begin():
        users = User.create_database(app.config.get('USERS'))
        orders = Order.create_database(app.config.get('ORDERS'))
        offers = Offer.create_database(app.config.get('OFFERS'))
        db.session.add_all(users)
        db.session.add_all(orders)
        db.session.add_all(offers)
    message = "Данные занесены в БД"
    return render_template('done.html', message=message)


@app.route('/create_db', methods=['GET'])
def db_create():
    db.create_all()
    message = "Таблицы БД созданы"
    return render_template('done.html', message=message)


@app.route('/drop_db', methods=['GET'])
def db_drop():
    db.drop_all()
    message = "Сброс БД выполнен"
    return render_template('done.html', message=message)


# --------------------------------


@app.route('/users', methods=['GET', 'POST'])
def users_all():
    if request.method == 'POST':
        with db.session.begin():
            user = User(**request.json)
            db.session.add(user)
        return jsonify(user.instance_to_dict())
    else:
        users = User.query.all()
        users_json = [user.instance_to_dict() for user in users]
        return jsonify(users_json)


@app.route('/users/<int:idx>', methods=['GET', 'PUT', 'DELETE'])
def user_id(idx: int):
    if request.method == 'PUT':
        data = request.json
        with db.session.begin():
            user = User.query.filter(User.id == idx).one()
            user.update(data)
        return jsonify(user.instance_to_dict())
    elif request.method == 'DELETE':
        with db.session.begin():
            User.query.filter(User.id == idx).delete()
        return redirect('/users', 302)
    else:
        user = User.query.filter(User.id == idx).one()
        return jsonify(user.instance_to_dict())


@app.route("/orders", methods=['GET', 'POST'])
def orders_all():
    if request.method == 'POST':
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


@app.route("/orders/<int:idx>", methods=['GET', 'PUT', 'DELETE'])
def order_by_id(idx):
    if request.method == 'PUT':
        data = request.json
        data_changed = Order.convert_date(data)
        with db.session.begin():
            order = Order.query.filter(Order.id == idx).one()
            order.update(data_changed)
        return jsonify(order.instance_to_dict())

    elif request.method == 'DELETE':
        with db.session.begin():
            Order.query.filter(Order.id == idx).delete()
        return redirect('/orders', 302)

    else:
        order = Order.query.filter(Order.id == idx).one()
        return jsonify(order.instance_to_dict())


@app.route("/offers", methods=['GET', 'POST'])
def offers_all():
    if request.method == 'POST':
        with db.session.begin():
            offer = Offer(**request.json)
            db.session.add(offer)
        return jsonify(offer.instance_to_dict())
    else:
        offers = Offer.query.all()
        offers_json = [offer.instance_to_dict() for offer in offers]
        return jsonify(offers_json)


@app.route("/offers/<int:idx>", methods=['GET', 'PUT', 'DELETE'])
def offer_by_id(idx):
    if request.method == 'PUT':
        data = request.json
        with db.session.begin():
            offer = Offer.query.filter(Offer.id == idx).one()
            offer.update(data)
        return jsonify(offer.instance_to_dict())

    elif request.method == 'DELETE':
        with db.session.begin():
            Offer.query.filter(Order.id == idx).delete()
        return redirect('/offers', 302)

    else:
        offer = Offer.query.filter(Offer.id == idx).one()
        return jsonify(offer.instance_to_dict())


if __name__ == '__main__':
    app.run()
