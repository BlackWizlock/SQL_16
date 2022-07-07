from flask import Flask, jsonify, render_template, request, redirect
from model import db, User, Order, Offer
import service

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


@app.route('/')
def index(): return render_template('index.html')


# Основной аггрегатор БД - создание таблиц, удаление таблиц, наполнение данными
@app.route('/add')
def db_index():
    service.fill_databases()
    message = "Данные занесены в БД"
    return render_template('done.html', message=message)


@app.route('/create_db', methods=['GET'])
def db_create():
    service.create_database()
    message = "Таблицы БД созданы"
    return render_template('done.html', message=message)


@app.route('/drop_db', methods=['GET'])
def db_drop():
    service.drop_databases()
    message = "Сброс БД выполнен"
    return render_template('done.html', message=message)


# --------------------------------


@app.route('/users', methods=['GET', 'POST'])
def users_all():
    return service.users_all(request.method)


@app.route('/users/<int:idx>', methods=['GET', 'PUT', 'DELETE'])
def users_id(idx: int):
    return service.users_id(idx, request.method)


@app.route("/orders", methods=['GET', 'POST'])
def orders_all():
    return service.orders_all(request.method)


@app.route("/orders/<int:idx>", methods=['GET', 'PUT', 'DELETE'])
def orders_by_id(idx):
    return service.orders_by_id(idx, request.method)


@app.route("/offers", methods=['GET', 'POST'])
def offers_all():
    return service.offers_all(request.method)


@app.route("/offers/<int:idx>", methods=['GET', 'PUT', 'DELETE'])
def offers_by_id(idx):
    return service.offers_by_id(idx, request.method)


if __name__ == '__main__':
    app.run()
