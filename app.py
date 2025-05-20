from flask import Flask, render_template, g, request, redirect, url_for, jsonify, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import math
from sqlalchemy.orm import sessionmaker
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask import abort
from flask import Flask, send_file, render_template



app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/Printing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Materials(db.Model):
    __tablename__ = 'materials'    
    id_materials = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

class Order(db.Model):
    __tablename__ = 'orders'
    id_order = db.Column(db.Integer, primary_key=True)
    name_orders = db.Column(db.Text)
    id_parent_operation = db.Column(db.Integer,db.ForeignKey('operations.id_operations'), primary_key=True)
    id_child_operation = db.Column(db.Integer, db.ForeignKey('operations.id_operations'), primary_key=True)
    amount = db.Column(db.Integer)
    circulation = db.Column(db.Integer)
    status = db.Column(db.Text)
    id_employee = db.Column(db.Integer)
    id_customers = db.Column(db.Integer)
    order_date = db.Column(db.Date)
    order_time = db.Column(db.Time)
    date_completion = db.Column(db.Date)
    time_completion = db.Column(db.Time)
    quantity_entrance = db.Column(db.Integer)
    number_operations = db.Column(db.Integer)
    defective = db.Column(db.Integer)
    quantity_output = db.Column(db.Integer)
    id_nomenclature_orders = db.Column(db.Integer, db.ForeignKey('nomenclature_orders.id_nomenclature_orders'))

class Employee(db.Model):
    __tablename__ = 'employee'
    id_employee = db.Column(db.Integer, primary_key=True, autoincrement=True)
    surname = db.Column(db.String, nullable=False)
    name_employee = db.Column(db.String, nullable=False)
    patronymic = db.Column(db.String)
    position_employee = db.Column(db.String, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True  

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id_employee)

    # @classmethod
    # def create_employee(cls, surname, name_employee, patronymic, position_employee, password):
    #     hashed_password = generate_password_hash(password)
    #     new_employee = cls(
    #         surname=surname,
    #         name_employee=name_employee,
    #         patronymic=patronymic,
    #         position_employee=position_employee,
    #         password=hashed_password
    #     )
    #     try:
    #         db.session.add(new_employee)
    #         db.session.commit()
    #     except Exception as e:
    #         db.session.rollback()  # Откат транзакции в случае ошибки
    #         print(f"Ошибка при создании сотрудника: {e}")
    #         return None  # Возвращаем None в случае ошибки
    #     return new_employee

    
    @classmethod
    def authenticate(cls, id_employee, password):
        employee = cls.query.filter_by(id_employee=id_employee).first()
        if employee:
            if check_password_hash(employee.password, password):
                return employee
            else:
                print("Пароль неверный")
        else:
            print("Пользователь не найден")
        return None
    
class Customers(db.Model):
    __tablename__ = 'customers'
    id_customer = db.Column(db.Integer, primary_key=True)
    name_customer = db.Column(db.String)
    contacts = db.Column(db.String)
    address = db.Column(db.String)

class Operation(db.Model):
    __tablename__ = 'operations'
    id_operations = db.Column(db.Integer, primary_key=True)
    name_operations = db.Column(db.String)
    id_materials = db.Column(db.Integer, db.ForeignKey('materials.id_materials'))
    number_materials = db.Column(db.Float)
    id_type_work = db.Column(db.Integer, db.ForeignKey('type_work.id_type_work'))
    id_coeff_cutting = db.Column(db.Integer, db.ForeignKey('coeff_cutting.id_coeff_cutting'))
    base = db.Column(db.Boolean)
    id_price = db.Column(db.Integer, db.ForeignKey('price_list.id_price'))
    processing = db.Column(db.String)
    id_nomenclature_operation = db.Column(db.Integer, db.ForeignKey('nomenclature_operation.id_nomenclature_operation'))
    quantity_in_one = db.Column(db.Float)
    decoding = db.Column(db.String)
    
class ParametersOperation(db.Model):
    __tablename__ = 'parameters_operations' 
    id_parameters = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    id_operations = db.Column(db.Integer, db.ForeignKey('operations.id_operations'))
    id_nomenclature_parameters = db.Column(db.Integer, db.ForeignKey('nomenclature_parameters.id_nomenclature_parameters'))
    value = db.Column(db.String)  
       
class CoeffCutting(db.Model):
    __tablename__ = 'coeff_cutting'
    id_coeff_cutting = db.Column(db.Integer, primary_key=True)
    name_coeff_cutting = db.Column(db.String)
    coeff_cutting = db.Column(db.Float)
    
class NomenclatureOrders(db.Model):
    __tablename__ = 'nomenclature_orders'
    id_nomenclature_orders = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_nomenclature_orders = db.Column(db.String)
    
class NomenclatureParameters(db.Model):
    __tablename__ = 'nomenclature_parameters'
    id_nomenclature_parameters = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_parameters = db.Column(db.String)

class TypeWork(db.Model):
    __tablename__ = 'type_work'
    id_type_work = db.Column(db.Integer, primary_key=True)
    name_type_work = db.Column(db.String)

class PriceList(db.Model):
    __tablename__ = 'price_list'    
    id_price = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    id_nomenclature_operation = db.Column(db.Integer, db.ForeignKey('nomenclature_operation.id_nomenclature_operation'))

class NomenclatureOperations(db.Model):
    __tablename__ = 'nomenclature_operation'    
    id_nomenclature_operation = db.Column(db.Integer, primary_key=True)
    name_nomenclature_operation = db.Column(db.String)

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class LoginForm(FlaskForm):
    name_employee = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

#получить дерево заказа с указанным id
def get_orders(order_id):
    try:
        # Установка соединения с базой данных
        with psycopg2.connect("dbname=Printing user=postgres password=1234") as conn:
            # Создание курсора для выполнения SQL-запросов
            with conn.cursor() as cur:
                # Выполнение SQL-запроса для получения информации о заказах по заданному ID
                cur.execute("""        
                    SELECT id_order, id_parent_operation, id_child_operation
                    FROM orders
                    WHERE id_order = %s
                """, (order_id,))
                orders = cur.fetchall()  # Получение всех результатов запроса
                return orders  # Возврат списка заказов
    except Exception as e:
        # Логирование ошибки при получении заказов
        print(f"Ошибка при получении заказов: {e}")
        return []  # Возврат пустого списка в случае ошибки

#получение стоимости заказа
def get_total_cost(order_id):
    # Установка соединения с базой данных
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()  # Создание курсора для выполнения SQL-запросов
    # Выполнение SQL-запроса для получения стоимости заказа по заданному ID
    cur.execute("""        
        SELECT amount
        FROM orders
        WHERE id_order = %s and id_parent_operation = 0
    """, (order_id,))
    cost = cur.fetchone()  # Получение результата запроса
    if cost:
        cost = cost[0]  # Извлечение стоимости из результата
    else:
        cost = 0  # Установка стоимости в 0, если результат пустой
    cur.close()  # Закрытие курсора
    conn.close()  # Закрытие соединения с базой данных
    return cost  # Возврат стоимости заказа

#получение тиража заказа
def get_circulation(order_id):
    # Установка соединения с базой данных
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()  # Создание курсора для выполнения SQL-запросов
    # Выполнение SQL-запроса для получения тиража заказа по заданному ID
    cur.execute("""        
        SELECT circulation
        FROM orders
        WHERE id_order = %s and id_parent_operation = 0
    """, (order_id,))
    circulation = cur.fetchone()  # Получение результата запроса
    if circulation:
        circulation = circulation[0]  # Извлечение тиража из результата
    else:
        circulation = 0  # Установка тиража в 0, если результат пустой
    cur.close()  # Закрытие курсора
    conn.close()  # Закрытие соединения с базой данных
    return circulation  # Возврат тиража заказа

#построение словаря родитель - дочерний элемент
def build_tree(orders):
    tree = {}  # Инициализация пустого словаря для дерева заказов
    for order in orders:  # Проход по всем заказам
        id_order, parent, child = order  # Извлечение ID заказа, ID родительской и ID дочерней операции
        if parent not in tree:
            tree[parent] = []  # Инициализация списка для родителя, если его еще нет в дереве
        # Добавление информации о заказе в дерево
        tree[parent].append({'id_order': id_order, 'id_child': child})
    return tree  # Возврат построенного дерева

def get_order_name_by_id(order_id):
    order = Order.query.filter_by(id_order=order_id, id_parent_operation=0).first()
    return order.name_orders if order else "Название не найдено"

def get_name_operations(id_child):
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    cur.execute("""        
            SELECT name_operations
            FROM operations
            WHERE id_operations = %s
    """, (id_child,))    
    orders = cur.fetchone()
    #print(f'{orders}')
    cur.close()
    conn.close()
    return orders[0]

def get_decoding_operations(id_child):
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    cur.execute("""        
            SELECT decoding
            FROM operations
            WHERE id_operations = %s
    """, (id_child,))    
    orders = cur.fetchone()
    if orders is None or orders[0] is None:
        decoding = ' '
    elif orders[0] =='':
        decoding = ' '
    else:
        decoding = f'({orders[0]})'
    #print(f'{orders}')
    cur.close()
    conn.close()
    return decoding

def get_quantity_output_operations(id_child, order_id):
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    cur.execute("""        
            SELECT quantity_output
            FROM orders
            WHERE id_child_operation = %s AND id_order = %s
    """, (id_child, order_id))    
    orders = cur.fetchone()
    #print(f'{orders}')
    cur.close()
    conn.close()
    return orders[0]

def get_materials_for_operation(operation_id):
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    #print(f'operation_id {operation_id}')
    cur.execute("""        
            SELECT id_materials
            FROM operations
            WHERE id_operations = %s
    """, (operation_id,))  
    orders = cur.fetchone()  
    #print(f'orders {orders}')
    if orders is not None:
        data = orders[0] 
    else:
        data = 0
    cur.close()
    conn.close()
    #print(f'data {data}')
    return data

#отрисовка дерева со статусом расчет
def render_tree(order_id, tree, operations, parent=0, visited=None):
    if visited is None:
        visited = set() # Инициализация множества для отслеживания посещенных узлов
    if parent in visited:
        # Проверка на циклические ссылки в дереве
        raise RecursionError(f"Cyclic reference detected at parent: {parent}")
    visited.add(parent) # Добавление текущего узла в посещенные
    html = ""   
    if parent == 0:
        # Получение названия заказа по его id
        order_name = get_order_name_by_id(order_id)
        html += f"<p class='order-info'>Название заказа: {order_name}</p>"
    if parent in tree:
        html += "<ul class='tree'>" # Начало списка для отображения дерева
        for child in tree[parent]:
            # Добавление информации о дочернем элементе
            html += f"<li><span class='caret'>{get_quantity_output_operations(child['id_child'], order_id)}шт - {get_name_operations(child['id_child'])} {get_decoding_operations(child['id_child'])}</span>"
            # Форма для добавления новой операции
            html += f"<form action='{url_for('add_operation')}' method='POST' class='inline-form'>"
            # html += "<select name='operation_id' required class='operation-select'>"
            # for operation in operations:
            #     html += f"<option value='{operation.id_operations}'>ID: {operation.id_operations} - {operation.name_operations}</option>"
            # html += "</select>"
            html += f"<input type='hidden' name='order_id' value='{child['id_order']}'>"
            html += f"<input type='hidden' name='parent_id' value='{child['id_child']}'>"
            # Кнопка для добавления операции
            html += """<button type="submit" class="btn btn-secondary btn-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"></path>
  <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"></path>
</svg>
              </button>"""
            # Форма для удаления операции
            html += "</form>"
            html += f"<form action='{url_for('delete_operation')}' method='POST' class='inline-form'>"
            html += f"<input type='hidden' name='operation_id' value='{child['id_child']}'>"
            html += f"<input type='hidden' name='order_id' value='{child['id_order']}'>"
            html += f"<input type='hidden' name='parent_id' value='{parent}'>"
            # Кнопка для удаления операции
            html += """<button type="submit" class="btn btn-secondary btn-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-circle" viewBox="0 0 16 16">
  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
  <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8"/>
</svg>
              </button>"""
            html += "</form>"
            # Форма для получения информации об операции
            html += "</form>"
            html += f"<form action='{url_for('about_operation', operation_id=child['id_child'])}' method='POST' class='inline-form'>"
            html += f"<input type='hidden' name='operation_id' value='{child['id_child']}'>"
            html += f"<input type='hidden' name='order_id' value='{child['id_order']}'>"
            html += f"<input type='hidden' name='parent_id' value='{parent}'>"
            # Кнопка для получения информации об операции
            html += """<button type="submit" class="btn btn-secondary btn-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bullseye" viewBox="0 0 16 16">
  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
  <path d="M8 13A5 5 0 1 1 8 3a5 5 0 0 1 0 10m0 1A6 6 0 1 0 8 2a6 6 0 0 0 0 12"/>
  <path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6m0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8"/>
  <path d="M9.5 8a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0"/>
</svg>
              </button>"""
            html += "</form>"
            # Рекурсивный вызов для отображения дочерних операций
            html += render_tree(order_id, tree, operations, child['id_child'], visited)
            html += "</li>"
        html += "</ul>"    
    return html # Возврат сгенерированного HTML-кода

#отрисовка проверенного дерева для других статусов
def render_tree_verified(order_id, tree, operations, parent=0, visited=None):
    if visited is None:
        visited = set() # Инициализация множества для отслеживания посещенных узлов
    if parent in visited:
        raise RecursionError(f"Cyclic reference detected at parent: {parent}")
    visited.add(parent) # Добавление текущего узла в посещенные
    html = ""   
    if parent == 0:
        # Получение названия заказа по его id
        order_name = get_order_name_by_id(order_id)
        html += f"<p> Название заказа: {order_name}</p>"
    if parent in tree:
        html += "<ul>" # Начало списка для отображения дерева
        for child in tree[parent]:
            print(f"child {child['id_child']}")
            # Добавление информации о дочернем элементе
            html += f"<li><span class='caret'>{get_quantity_output_operations(child['id_child'], order_id)}шт - {get_name_operations(child['id_child'])} {get_decoding_operations(child['id_child'])}</span>"
            # Форма для получения информации об операции
            html += f"<form action='{url_for('about_operation', operation_id=child['id_child'])}' method='POST' class='inline-form'>"
            html += f"<input type='hidden' name='operation_id' value='{child['id_child']}'>" # Скрытое поле с id операции
            html += f"<input type='hidden' name='order_id' value='{child['id_order']}'>" # Скрытое поле с id заказа
            html += f"<input type='hidden' name='parent_id' value='{parent}'>" # Скрытое поле с id родителя
            # Кнопка для получения информации об операции
            html += """<button type="submit" class="btn btn-secondary btn-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bullseye" viewBox="0 0 16 16">
  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
  <path d="M8 13A5 5 0 1 1 8 3a5 5 0 0 1 0 10m0 1A6 6 0 1 0 8 2a6 6 0 0 0 0 12"/>
  <path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6m0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8"/>
  <path d="M9.5 8a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0"/>
</svg>
              </button>"""
            html += "</form>"
            # Рекурсивный вызов для отображения дочерних операций
            html += render_tree_verified(order_id, tree, operations, child['id_child'], visited)
            html += "</li>"
        html += "</ul>"    
    return html # Возврат сгенерированного HTML-кода

def render_tree_pdf(order_id, tree, operations, parent=0, visited=None):
    if visited is None:
        visited = set()
    if parent in visited:
        raise RecursionError(f"Cyclic reference detected at parent: {parent}")
    visited.add(parent)
    html = ""   
    if parent == 0:
        order_name = get_order_name_by_id(order_id)
        html += f"<p>Название заказа: {order_name}</p>"
    if parent in tree:
        html += "<ul>"
        for child in tree[parent]:
            operation_id = child['id_child']
            html += f"<li><span class='caret'>{get_quantity_output_operations(operation_id, order_id)}шт - {get_name_operations(operation_id)} {get_decoding_operations(operation_id)}</span>"
            # Получение и вывод материалов для текущей операции
            id_materials = get_materials_for_operation(operation_id)
            if id_materials!=0:                
                materials = get_materials_for_order(order_id)
                if materials:
                    html += "<ul>"
                    for material in materials:
                        print(f'id_materials {id_materials} material {material["id_materials"]}')
                        if id_materials == int(material['id_materials']):
                            html += f"<li>{int(material['количество'])}шт - {material['name']}</li>"  # Предполагается, что 'name' и 'quantity' являются ключами в словаре материала
                    html += "</ul>"
            
            html += render_tree_pdf(order_id, tree, operations, operation_id, visited)
            html += "</li>"
        html += "</ul>"    
    return html


def update_order(cur, order_id, circulation):
    # Получаем информацию о родительской операции
    cur.execute("""
        SELECT id_child_operation
        FROM orders
        WHERE id_order = %s AND id_parent_operation = 0
    """, (order_id,))
    parent_info = cur.fetchone()
    value = None

    if parent_info:
        child_id = parent_info
        #обновляем значение тиража
        cur.execute("""
            UPDATE orders
            SET circulation = %s
            WHERE id_order = %s AND id_parent_operation = 0
        """, (circulation, order_id))
        #получаем параметры операции
        cur.execute("""
            SELECT processing
            FROM operations
            WHERE id_operations = (SELECT id_child_operation FROM orders WHERE id_order = %s AND id_parent_operation = 0)
        """, (order_id,))
        operation = cur.fetchone()
        if operation:
            processing = operation[0]
            print(f'РОдительская операция {processing}')
            defective_percentage = 0
            defective_material = 0 
            defective_percentage_result = ParametersOperation.query.filter_by(id_nomenclature_parameters=2, id_operations=child_id).first()
            if defective_percentage_result is not None:
                defective_percentage = float(defective_percentage_result.value)
            else:
                defective_percentage = 0
            defective_material_result = ParametersOperation.query.filter_by(id_nomenclature_parameters=1, id_operations=child_id).first()
            if defective_material_result is not None:
                defective_material = int(defective_material_result.value)
            else:
                defective_material = 0
            
            if processing == 'Фотовывод':
                result = ParametersOperation.query.filter_by(id_nomenclature_parameters=3, id_operations=child_id).first()
                if result:
                    print(f'result {result}')
                    value = result.value
                    print(f'value {value}')
                    # Разделяем строку по символу '+'
                    parts = value.split('+')
                    # Преобразуем каждую часть в целое число
                    int_values = [int(part) for part in parts]
                    # Если вам нужно сложить значения
                    colors = sum(int_values)                
                    print(f'colors {colors}')
                else:
                    colors = 1
                quantity_entrance = colors
                number_operations = colors
                quantity_output = colors
                defective = 0   
                print(f'quantity_entrance {quantity_entrance} number_operations {number_operations} quantity_output {quantity_output} defective {defective}')
            elif processing == 'Печать':
                result = ParametersOperation.query.filter_by(id_nomenclature_parameters=3, id_operations=child_id).first()
                print(f'result {result}')
                value = result.value
                print(f'value {value}')
                # Разделяем строку по символу '+'
                parts = value.split('+')
                # Преобразуем каждую часть в целое число
                int_values = [int(part) for part in parts]
                # Если вам нужно сложить значения
                colors = sum(int_values)
                print(f'colors {colors}')
                number_operations = circulation
                quantity_output = circulation
                defective = math.ceil(number_operations * defective_percentage / 100 + defective_material * colors)                
                quantity_entrance = circulation + defective
            elif processing == 'Резка':
                print(f'Резка')
                # Получение параметров для операции "Резка"
                result = ParametersOperation.query.filter_by(id_nomenclature_parameters=4, id_operations=child_id).first()
                cutting_parts = int(result.value)
                # if result is not None:
                #     print(f'result {result}')
                #     # Проверяем, что value существует и является числом
                #     if result.value is not None:
                #         cutting_parts = int(result.value)
                #     else:
                #         cutting_parts = 1  # Используем значение по умолчанию
                #     print(f'cutting_parts: {cutting_parts}')
                # else:
                #     cutting_parts = 1  # Значение по умолчанию, если параметр не найден
                print(f'cutting parts {cutting_parts}')
                # Проверка circulation перед использованием
                if circulation is not None and isinstance(circulation, (int, float)) and cutting_parts > 0:
                    number_operations = math.ceil(circulation / cutting_parts)
                    defective = math.ceil(number_operations * defective_percentage / 100 + defective_material)
                    quantity_output = circulation
                    quantity_entrance = circulation + defective

                    print(f'number_operations: {number_operations}, defective: {defective}, quantity_output: {quantity_output}, quantity_entrance: {quantity_entrance}')
                else:
                    print("Ошибка: circulation или cutting_parts некорректны.")


            else:
                number_operations = circulation
                defective = math.ceil(number_operations * defective_percentage / 100 + defective_material)
                quantity_output = circulation
                quantity_entrance = circulation + defective             
              
        # Обновляем дополнительные поля
        cur.execute("""
            UPDATE orders
            SET quantity_output = %s,
                quantity_entrance = %s,
                number_operations = %s,
                defective = %s
            WHERE id_order = %s AND id_parent_operation = 0
        """, (quantity_output, quantity_entrance, number_operations, defective, order_id))     
        
        # Получаем все дочерние операции
        cur.execute("""
            SELECT id_parent_operation, id_child_operation
            FROM orders
            WHERE id_parent_operation = (SELECT id_child_operation FROM orders WHERE id_parent_operation = 0 and id_order = %s) AND id_order = %s
        """, (order_id, order_id))  
        child_orders = cur.fetchall()

        # Рекурсивно обновляем дочерние заказы
        for child_order in child_orders:
            parent_order_id = child_order[0]
            child_order_id = child_order[1]
            update_child_orders(cur, order_id, parent_order_id, child_order_id, circulation)

def update_child_orders(cur, order_id, parent_id, child_id, parent_quantity_entrance):
    print(f'')
    print(f'Номер операции {child_id} {get_name_operations(child_id)} родительская операция {parent_id} {get_name_operations(parent_id)}')
    print(f'Количество на входе {parent_quantity_entrance}')
    quantity_entrance = parent_quantity_entrance
   # Получаем данные из таблицы operations для текущего заказа
    cur.execute("""
        SELECT processing, quantity_in_one
        FROM operations
        WHERE id_operations = %s
    """, (child_id,))
    operation = cur.fetchone()
    value = None
    if operation:
        processing, quantity_in_one = operation
        print(f'Операция {child_id}    {processing}')
        # Инициализация значений по умолчанию
        defective_percentage = 0
        defective_material = 0 

        # Получение значения defective_percentage
        defective_percentage_result = ParametersOperation.query.filter_by(id_nomenclature_parameters=2, id_operations=child_id).first()
        if defective_percentage_result is not None and defective_percentage_result.value is not None:
            try:
                defective_percentage = float(defective_percentage_result.value)
            except ValueError:
                print(f"Ошибка преобразования defective_percentage: {defective_percentage_result.value}")
                defective_percentage = 0  # Устанавливаем значение по умолчанию в случае ошибки преобразования
        else:
            defective_percentage = 0
        print(f'defective_percentage {defective_percentage}')
        # Получение значения defective_material
        defective_material_result = ParametersOperation.query.filter_by(id_nomenclature_parameters=1, id_operations=child_id).first()
        if defective_material_result is not None and defective_material_result.value is not None:
            try:
                defective_material = int(defective_material_result.value)
            except ValueError:
                print(f"Ошибка преобразования defective_material: {defective_material_result.value}")
                defective_material = 0  # Устанавливаем значение по умолчанию в случае ошибки преобразования
        else:
            defective_material = 0
        print(f'defective_material {defective_material}')

        
        if processing == 'Фотовывод':
            print(f'Фотовывод ')
            result = ParametersOperation.query.filter_by(id_nomenclature_parameters=3, id_operations=child_id).first()
            if result:
                print(f'result {result}')
                value = result.value
                print(f'value {value}')
                # Разделяем строку по символу '+'
                parts = value.split('+')
                # Преобразуем каждую часть в целое число
                int_values = [int(part) for part in parts]
                # Если вам нужно сложить значения
                colors = sum(int_values)                
                print(f'colors {colors}')
            else:
                value = 1
            quantity_entrance = colors 
            number_operations = colors
            quantity_output = colors * quantity_in_one
            defective = 0   
            print(f'quantity_entrance {quantity_entrance} number_operations {number_operations} quantity_output {quantity_output} defective {defective}')
        elif processing == 'Печать':
            result = ParametersOperation.query.filter_by(id_nomenclature_parameters=3, id_operations=child_id).first()
            print(f'Печать ')
            if result is not None:
                print(f'result {result}')
                value = result.value
                
                if value is not None:  # Проверяем, что value не равно None
                    print(f'value {value}')
                    # Разделяем строку по символу '+'
                    parts = value.split('+')
                    # Преобразуем каждую часть в целое число
                    int_values = [int(part) for part in parts if part.isdigit()]  # Проверяем, что part - это число
                    # Если вам нужно сложить значения
                    colors = sum(int_values)
                else:
                    colors = 1  # Значение по умолчанию, если value равно None
            else:
                colors = 1  # Значение по умолчанию, если result равно None

            number_operations = parent_quantity_entrance
            quantity_output = parent_quantity_entrance * quantity_in_one 
            defective = math.ceil(number_operations * defective_percentage / 100 + defective_material * colors)                
            quantity_entrance = (parent_quantity_entrance + defective) 

        elif processing == 'Резка':
            result = ParametersOperation.query.filter_by(id_nomenclature_parameters=4, id_operations=child_id).first()
            print(f'Резка ')
            if result is not None:
                print(f'result {result}')
                
                # Проверка на None и преобразование
                if result.value is not None and result.value.isdigit():
                    cutting_parts = int(result.value)
                else:
                    cutting_parts = 1  # Значение по умолчанию, если value пустое или некорректное
            else:
                cutting_parts = 1  # Значение по умолчанию, если параметр не найден
            print(f'cutting parts {cutting_parts} ')
            # Проверка на корректность parent_quantity_entrance перед использованием
            if parent_quantity_entrance is not None and cutting_parts > 0:
                print(f'parent_quantity_entrance {parent_quantity_entrance}')
                number_operations = math.ceil(parent_quantity_entrance / cutting_parts)
                print(f'number_operations {number_operations}')
                defective = math.ceil(number_operations * defective_percentage / 100 + defective_material)
                print(f'defective {defective}')
                quantity_output = parent_quantity_entrance * quantity_in_one
                print(f'quantity_output {quantity_output}')
                quantity_entrance = (math.ceil(quantity_output / cutting_parts) + defective) 
                print(f'quantity_entrance {quantity_entrance}')
            else:
                print("Ошибка: parent_quantity_entrance или cutting_parts некорректны.")

        else:
            number_operations = parent_quantity_entrance
            defective = math.ceil(number_operations * defective_percentage / 100 + defective_material)
            quantity_output = parent_quantity_entrance * quantity_in_one
            quantity_entrance = (parent_quantity_entrance + defective) 
        
        cur.execute("""
            UPDATE orders
            SET quantity_entrance = %s,
                number_operations = %s,
                defective = %s,
                quantity_output = %s
            WHERE id_order = %s AND id_parent_operation = %s AND id_child_operation = %s
        """, (quantity_entrance, number_operations, defective, quantity_output, order_id, parent_id, child_id)) 

    if cur.rowcount == 0:
        print(f"Дочерний заказ с id_order {order_id} не найден или не обновлен.")

    # Получаем все дочерние операции
    cur.execute("""
        SELECT id_parent_operation, id_child_operation
        FROM orders
        WHERE id_parent_operation = %s AND id_order = %s
    """, (child_id, order_id))  
    child_orders = cur.fetchall()

    # Рекурсивно обновляем дочерние заказы
    for child_order in child_orders:
        parent_order_id = child_order[0]
        child_order_id = child_order[1]
        update_child_orders(cur, order_id, parent_order_id, child_order_id, quantity_entrance)

#стоимость заказа
def calculate_order_amount(cur, order_id):
    print(f'Стоимость родительскогго элемента')
    total_price = 0  
    print(f'Общая стоимость {total_price}')
    cur.execute("""
    SELECT quantity_output
    FROM orders
    WHERE id_order = %s AND id_parent_operation = %s
    """, (order_id, 0))
    quantity_output = cur.fetchone()

    # Проверка результата
    if quantity_output:
        quantity_output_k = quantity_output[0] 
        print(f'количество на выходе {quantity_output}')
    else:
        print("Нет данных для quantity_output, устанавливаем в 0")
        quantity_output = 0  
    cur.execute("""
        SELECT id_child_operation
        FROM orders
        WHERE id_order = %s AND id_parent_operation = 0
    """, (order_id,))
    parent_info = cur.fetchone()
    if parent_info:
        child_operation_id = parent_info[0]
        cur.execute("""
            SELECT id_materials, id_price, id_coeff_cutting
            FROM operations
            WHERE id_operations = %s
        """, (child_operation_id,))
        result = cur.fetchone()
        if result:
            material, id_price, id_coeff_cutting = result
        else:
            material = None
            id_price = None
            id_coeff_cutting = None

        print(f'material {material}')
        if material:
            print(f'id материал {material}')
            cur.execute("""
                SELECT price
                FROM materials
                WHERE id_materials = %s
            """, (material,))  # Передаем id_materials
            price_material = cur.fetchone()
            print(f'    Стоимость материала {price_material}')
            
            total_price += price_material[0] * quantity_output_k
            print(f'        Общая стоимость после добовления стоимости материала {total_price}')

        # Получаем данные из таблицы price_list для текущего заказа
        cur.execute("""
            SELECT amount
            FROM price_list
            WHERE id_price = %s
        """, (id_price,))
        price_operation = cur.fetchone()
        
        if price_operation:
            if id_coeff_cutting:
                cutting_coeff = CoeffCutting.query.filter_by(id_coeff_cutting = id_coeff_cutting)
                print(f'    Стоимость операции {price_operation}')
                total_price += price_operation[0] * cutting_coeff.value # Добавляем стоимость операции
                print(f'        Общая стоимость после добовления стоимости операции {total_price}')
            else:
                print(f'    Стоимость операции {price_operation}')
                total_price += price_operation[0]  # Добавляем стоимость операции
                print(f'        Общая стоимость после добовления стоимости операции {total_price}')

        # Получаем все дочерние операции
        cur.execute("""
            SELECT id_child_operation
            FROM orders
            WHERE id_parent_operation = %s and id_order = %s
        """, (child_operation_id, order_id))  
        child_orders = cur.fetchall()

        # Рекурсивно обновляем дочерние заказы
        for child_order in child_orders:
            parent_order_id = child_operation_id
            child_order_id = child_order[0]
            total_price += calculate_order_child_amount(cur, order_id, parent_order_id, child_order_id)

    return total_price

def calculate_order_child_amount(cur, order_id, parent_order_id, child_order_id):
    print(f'Стоимость РОДИТЕЛЬСКИЙ {parent_order_id} ДОЧЕРНИЙ {child_order_id} ')
    total_price = 0  
    
    cur.execute("""
    SELECT quantity_entrance
    FROM orders
    WHERE id_order = %s AND id_parent_operation = %s AND id_child_operation = %s
    """, (order_id, parent_order_id, child_order_id,))
    
    quantity_entrance = cur.fetchone()

    # Проверка результата
    if quantity_entrance and quantity_entrance[0] is not None:
        quantity_entrance_k = quantity_entrance[0]  
        print(f'Количество на входе = {quantity_entrance_k}')
    else:
        print("Нет данных для quantity_entrance, устанавливаем в 0")
        quantity_entrance_k = 0  # Установите значение по умолчанию   

    if child_order_id:
        # Получаем данные из таблицы operations для текущего заказа
        cur.execute("""
            SELECT id_materials, id_price
            FROM operations
            WHERE id_operations = %s
        """, (child_order_id,))
        result = cur.fetchone()
        if result:
            material, id_price = result
        else:
            material = None
            id_price = None
        print(f'    id материала {material}')
        if material: 
            cur.execute("""
                SELECT price
                FROM materials
                WHERE id_materials = %s
            """, (material,))  
            price_material = cur.fetchone()

            if price_material is not None and len(price_material) > 0: 
                print(f'        Стоимость материала {price_material[0]}')                
                total_price += price_material[0] * quantity_entrance_k
                print(f'            Стоимость после добавления стоимости материала {total_price}')
            else:
                print("Нет данных для стоимости материала.")
        else:
            print("Нет данных для материала.")

        cur.execute("""
            SELECT amount
            FROM price_list
            WHERE id_price = %s
        """, (id_price,))
        price_operation = cur.fetchone()

        if price_operation:
            print(f'        Стоимость операции {price_operation[0]}')            
            total_price += price_operation[0] 
            print(f'            Стоимость после добовления стоимости операции {total_price}')

        cur.execute("""
            SELECT id_parent_operation, id_child_operation
            FROM orders
            WHERE id_parent_operation = %s and id_order = %s
        """, (child_order_id, order_id))  
        child_orders = cur.fetchall()
        print(f'Дочерние элементы {child_orders}')
        # Рекурсивно обновляем дочерние заказы
        for child_order in child_orders:
            parent_order_id = child_order[0]
            child_order_id = child_order[1]
            print(f'Родительский {parent_order_id} Дочерний {child_order_id}')
            total_price += calculate_order_child_amount(cur, order_id, parent_order_id, child_order_id)      
        
    return total_price

#стоимость материалов
def calculate_order_amount_material(cur, order_id):
    #print(f'Стоимость родительскогго элемента')
    total_price = 0  
    #print(f'Общая стоимость {total_price}')
    cur.execute("""
    SELECT quantity_output
    FROM orders
    WHERE id_order = %s AND id_parent_operation = %s
    """, (order_id, 0))
    quantity_output = cur.fetchone()

    # Проверка результата
    if quantity_output is not None and len(quantity_output) > 0:
        quantity_output = quantity_output[0] 
    else:
        print("Нет данных для quantity_output, устанавливаем в 0")
    quantity_output = 0  
    cur.execute("""
        SELECT id_child_operation
        FROM orders
        WHERE id_order = %s AND id_parent_operation = 0
    """, (order_id,))
    parent_info = cur.fetchone()
    if parent_info:
        child_operation_id = parent_info[0]
        cur.execute("""
            SELECT id_materials
            FROM operations
            WHERE id_operations = %s
        """, (child_operation_id,))
        material = cur.fetchone()
        #print(f'material {material}')
        if material[0]:
            #print(f'id материал {material}')
            cur.execute("""
                SELECT price
                FROM materials
                WHERE id_materials = %s
            """, (material[0],))  # Передаем id_materials
            price_material = cur.fetchone()
            #print(f'    Стоимость материала {price_material}')
            
            total_price += price_material[0] * quantity_output
            #print(f'        Общая стоимость после добовления стоимости материала {total_price}')

        # Получаем данные из таблицы price_list для текущего заказа
        # cur.execute("""
        #     SELECT amount
        #     FROM price_list
        #     WHERE id_operation = %s
        # """, (child_operation_id,))
        # price_operation = cur.fetchone()
        
        #if price_operation:
            #print(f'    Стоимость операции {price_operation}')
            #total_price += price_operation[0]  # Добавляем стоимость операции
            #print(f'        Общая стоимость после добовления стоимости операции {total_price}')

        # Получаем все дочерние операции
        cur.execute("""
            SELECT id_child_operation
            FROM orders
            WHERE id_parent_operation = %s and id_order = %s
        """, (child_operation_id, order_id))  
        child_orders = cur.fetchall()

        # Рекурсивно обновляем дочерние заказы
        for child_order in child_orders:
            parent_order_id = child_operation_id
            child_order_id = child_order[0]
            total_price += calculate_order_child_amount(cur, order_id, parent_order_id, child_order_id)

    return total_price

def calculate_order_child_amount_material(cur, order_id, parent_order_id, child_order_id):
    print(f'Стоимость РОДИТЕЛЬСКИЙ {parent_order_id} ДОЧЕРНИЙ {child_order_id} ')
    total_price = 0  
    
    cur.execute("""
    SELECT quantity_entrance
    FROM orders
    WHERE id_order = %s AND id_parent_operation = %s AND id_child_operation = %s
    """, (order_id, parent_order_id, child_order_id, ))
    quantity_entrance = cur.fetchone()
    print(f'Количество на входе = {quantity_entrance}')
    #Проверка результата
    if quantity_entrance is not None and len(quantity_entrance) > 0:
        quantity_entrance_k = quantity_entrance[0]  
        #print(f'quantity_entrance={quantity_entrance_k}')
    else:
        #print("Нет данных для quantity_entrance, устанавливаем в 0")
        quantity_entrance_k = 0  # Установите значение по умолчанию    

    if child_order_id:
        # Получаем данные из таблицы operations для текущего заказа
        cur.execute("""
            SELECT id_materials
            FROM operations
            WHERE id_operations = %s
        """, (child_order_id,))
        material = cur.fetchone()
        print(f'    id материала {material}')
        if material is not None and len(material) > 0 and material[0]: 
            cur.execute("""
                SELECT price
                FROM materials
                WHERE id_materials = %s
            """, (material[0],))  
            price_material = cur.fetchone()

            if price_material is not None and len(price_material) > 0: 
                print(f'        Стоимость материала {price_material[0]}')                
                total_price += price_material[0] * quantity_entrance_k
                print(f'            Стоимость после добавления стоимости материала {total_price}')
            else:
                print("Нет данных для стоимости материала.")
        else:
            print("Нет данных для материала.")

        # cur.execute("""
        #     SELECT amount
        #     FROM price_list
        #     WHERE id_operation = %s
        # """, (child_order_id,))
        # price_operation = cur.fetchone()

        #if price_operation:
            #print(f'        Стоимость операции {price_operation[0]}')            
            #total_price += price_operation[0] 
            #print(f'            Стоимость после добовления стоимости операции {total_price}')

        cur.execute("""
            SELECT id_parent_operation, id_child_operation
            FROM orders
            WHERE id_parent_operation = %s and id_order = %s
        """, (child_order_id, order_id))  
        child_orders = cur.fetchall()
        print(f'Дочерние элементы {child_orders}')
        # Рекурсивно обновляем дочерние заказы
        for child_order in child_orders:
            parent_order_id = child_order[0]
            child_order_id = child_order[1]
            print(f'Родительский {parent_order_id} Дочерний {child_order_id}')
            total_price += calculate_order_child_amount(cur, order_id, parent_order_id, child_order_id)      
        
    return total_price

#стоимость операций
def calculate_order_amount_operation(cur, order_id):
    #print(f'Стоимость родительскогго элемента')
    total_price = 0  
    #print(f'Общая стоимость {total_price}')
    # cur.execute("""
    # SELECT quantity_output
    # FROM orders
    # WHERE id_order = %s AND id_parent_operation = %s
    # """, (order_id, 0))
    # quantity_output = cur.fetchone()

    # # Проверка результата
    # if quantity_output is not None and len(quantity_output) > 0:
    #     quantity_output = quantity_output[0] 
    # else:
    #     print("Нет данных для quantity_output, устанавливаем в 0")
    # quantity_output = 0  
    cur.execute("""
        SELECT id_child_operation
        FROM orders
        WHERE id_order = %s AND id_parent_operation = 0
    """, (order_id,))
    parent_info = cur.fetchone()
    if parent_info:
        child_operation_id = parent_info[0]
        cur.execute("""
            SELECT id_price
            FROM operations
            WHERE id_operations = %s
        """, (child_operation_id,))
        id_price = cur.fetchone()
        # #print(f'material {material}')
        # if material[0]:
        #     #print(f'id материал {material}')
        #     cur.execute("""
        #         SELECT price
        #         FROM materials
        #         WHERE id_materials = %s
        #     """, (material[0],))  # Передаем id_materials
        #     price_material = cur.fetchone()
        #     #print(f'    Стоимость материала {price_material}')
            
        #     total_price += price_material[0] * quantity_output
        #     #print(f'        Общая стоимость после добовления стоимости материала {total_price}')

        # Получаем данные из таблицы price_list для текущего заказа
        cur.execute("""
            SELECT amount
            FROM price_list
            WHERE id_price = %s
        """, (id_price,))
        price_operation = cur.fetchone()
        
        if price_operation:
            #print(f'    Стоимость операции {price_operation}')
            total_price += price_operation[0]  # Добавляем стоимость операции
            #print(f'        Общая стоимость после добовления стоимости операции {total_price}')

        # Получаем все дочерние операции
        cur.execute("""
            SELECT id_child_operation
            FROM orders
            WHERE id_parent_operation = %s and id_order = %s
        """, (child_operation_id, order_id))  
        child_orders = cur.fetchall()

        # Рекурсивно обновляем дочерние заказы
        for child_order in child_orders:
            parent_order_id = child_operation_id
            child_order_id = child_order[0]
            total_price += calculate_order_child_amount_operation(cur, order_id, parent_order_id, child_order_id)

    return total_price

def calculate_order_child_amount_operation(cur, order_id, parent_order_id, child_order_id):
    print(f'Стоимость РОДИТЕЛЬСКИЙ {parent_order_id} ДОЧЕРНИЙ {child_order_id} ')
    total_price = 0  
    
    # cur.execute("""
    # SELECT quantity_entrance
    # FROM orders
    # WHERE id_order = %s AND id_parent_operation = %s AND id_child_operation = %s
    # """, (order_id, parent_order_id, child_order_id, ))
    # quantity_entrance = cur.fetchone()
    # print(f'Количество на входе = {quantity_entrance}')
    # #Проверка результата
    # if quantity_entrance is not None and len(quantity_entrance) > 0:
    #     quantity_entrance_k = quantity_entrance[0]  
    #     #print(f'quantity_entrance={quantity_entrance_k}')
    # else:
    #     #print("Нет данных для quantity_entrance, устанавливаем в 0")
    #     quantity_entrance_k = 0  # Установите значение по умолчанию    

    if child_order_id:
        # Получаем данные из таблицы operations для текущего заказа
        # cur.execute("""
        #     SELECT id_materials
        #     FROM operations
        #     WHERE id_operations = %s
        # """, (child_order_id,))
        # material = cur.fetchone()
        # print(f'    id материала {material}')
        # if material is not None and len(material) > 0 and material[0]: 
        #     cur.execute("""
        #         SELECT price
        #         FROM materials
        #         WHERE id_materials = %s
        #     """, (material[0],))  
        #     price_material = cur.fetchone()

        #     if price_material is not None and len(price_material) > 0: 
        #         print(f'        Стоимость материала {price_material[0]}')                
        #         total_price += price_material[0] * quantity_entrance_k
        #         print(f'            Стоимость после добавления стоимости материала {total_price}')
        #     else:
        #         print("Нет данных для стоимости материала.")
        # else:
        #     print("Нет данных для материала.")

        cur.execute("""
            SELECT amount
            FROM price_list
            WHERE id_operation = %s
        """, (child_order_id,))
        price_operation = cur.fetchone()

        if price_operation:
            print(f'        Стоимость операции {price_operation[0]}')            
            total_price += price_operation[0] 
            print(f'            Стоимость после добовления стоимости операции {total_price}')

        cur.execute("""
            SELECT id_parent_operation, id_child_operation
            FROM orders
            WHERE id_parent_operation = %s and id_order = %s
        """, (child_order_id, order_id))  
        child_orders = cur.fetchall()
        print(f'Дочерние элементы {child_orders}')
        # Рекурсивно обновляем дочерние заказы
        for child_order in child_orders:
            parent_order_id = child_order[0]
            child_order_id = child_order[1]
            print(f'Родительский {parent_order_id} Дочерний {child_order_id}')
            total_price += calculate_order_child_amount_operation(cur, order_id, parent_order_id, child_order_id)      
        
    return total_price

#копирование заказа
def copy_order(order_id):
    print(f'КОПИРОВАНИЕ ЗАКАЗА')
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    
    try:
        # Извлекаем данные заказа
        cur.execute("""
            SELECT name_orders, id_child_operation, amount, circulation, quantity_entrance, quantity_output, number_operations, defective, id_nomenclature_orders
            FROM orders
            WHERE id_order = %s and id_parent_operation = 0
        """, (order_id,))
        order_data = cur.fetchone()

        if not order_data:
            return f"Заказ с id_order {order_id} не найден."
        
        name_orders, id_child_operation, amount, circulation, quantity_entrance, quantity_output, number_operations, defective, id_nomenclature_orders = order_data
        print(f'первая операция {id_child_operation} заказа {order_id} название заказа {name_orders}')

        # Получаем новый уникальный id_order
        new_order_id = get_new_order_id(cur)
        print(f'новый id заказа {new_order_id}')
        
        new_child_operation = copy_operation(id_child_operation) #новый id родительской операции
        
        # Вставляем новую запись
        cur.execute("""
            INSERT INTO orders (id_order, name_orders, id_parent_operation, id_child_operation, amount, circulation, quantity_entrance, quantity_output, status, number_operations, defective, id_nomenclature_orders)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (new_order_id, name_orders, 0, new_child_operation, amount, circulation, quantity_entrance, quantity_output, 'расчет', number_operations, defective, id_nomenclature_orders))
        print(f'добавлена первая операция')

        # Получаем все дочерние операции
        cur.execute("""
            SELECT id_parent_operation, id_child_operation
            FROM orders
            WHERE id_parent_operation = (SELECT id_child_operation FROM orders WHERE id_parent_operation = 0 and id_order = %s) AND id_order = %s
        """, (order_id, order_id))  
        child_orders = cur.fetchall()
        
        new_parent_operation = new_child_operation

        # Рекурсивно обновляем дочерние заказы
        for child_order in child_orders:
            print(f'{child_order}')
            parent_order_id = child_order[0] #родит опер
            print(f'{child_order[0]}')
            child_order_id = child_order[1] #дочер опер
            print(f'{child_order[1]}')
            copy_order_child(order_id, name_orders, parent_order_id, child_order_id, new_order_id, new_parent_operation)
            
        conn.commit()
        return new_order_id

    except Exception as e:
        conn.rollback()
        return f"Ошибка при копировании заказа: {e}"
    finally:
        cur.close()
        conn.close()

def copy_order_child(order_id, name_orders, parent_order_id, id_child_operation, new_order_id, new_parent_operation):
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    
    cur.execute("""
            SELECT name_orders, id_child_operation, amount, circulation, quantity_entrance, quantity_output, number_operations, defective, id_nomenclature_orders
            FROM orders
            WHERE id_order = %s and id_parent_operation = %s and id_child_operation = %s
        """, (order_id, parent_order_id, id_child_operation))
    order_data = cur.fetchone()

    if not order_data:
        return f"Заказ с id_order {order_id} не найден."
        
    name_orders, id_child_operation, amount, circulation, quantity_entrance, quantity_output, number_operations, defective, id_nomenclature_orders = order_data
    print(f'первая операция {id_child_operation} заказа {order_id} название заказа {name_orders}')
    
    new_child_operation = copy_operation(id_child_operation)
    
    try:
        # Вставляем новую запись
        cur.execute("""
            INSERT INTO orders (id_order, name_orders, id_parent_operation, id_child_operation, amount, circulation, quantity_entrance, quantity_output, number_operations, defective, id_nomenclature_orders)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (new_order_id, name_orders, new_parent_operation, new_child_operation, amount, circulation, quantity_entrance, quantity_output, number_operations, defective, id_nomenclature_orders))

        # Получаем все дочерние операции
        cur.execute("""
            SELECT id_parent_operation, id_child_operation
            FROM orders
            WHERE id_parent_operation = %s AND id_order = %s
        """, (id_child_operation, order_id))  
        child_orders = cur.fetchall()
        
        new_parent_operation = new_child_operation

        # Рекурсивно обновляем дочерние заказы
        for child_order in child_orders:
            print(f'{child_order}')
            parent_order_id = child_order[0]
            print(f'{child_order[0]}')
            child_order_id = child_order[1]
            print(f'{child_order[1]}')
            copy_order_child(order_id, name_orders, parent_order_id, child_order_id, new_order_id, new_parent_operation)

        conn.commit()
        return f"Заказ {order_id} скопирован с новым id_order {new_order_id}."

    except Exception as e:
        conn.rollback()
        return f"Ошибка при копировании заказа: {e}"
    finally:
        cur.close()
        conn.close()

#копирование операции
def copy_operation(operation_id):
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()        
    operation = Operation.query.filter_by(id_operations=operation_id).first()
    print(f'{operation}')
    new_operation_id = get_new_operation_id()
    print(f'new_operation_id {new_operation_id}')
    new_parameters = Operation(
        id_operations = new_operation_id,
        name_operations=operation.name_operations,
        id_coeff_cutting=operation.id_coeff_cutting,
        id_type_work=operation.id_type_work,
        processing=operation.processing,
        id_price=operation.id_price,
        id_materials = operation.id_materials,
        number_materials = operation.number_materials,
        quantity_in_one = operation.quantity_in_one,
        decoding = operation.decoding
        )
    db.session.add(new_parameters)  # Добавление параметра в сессию    
    db.session.commit()  # Сохранение всех изменений
    
    # Получение всех параметров операции
    parameters_operations = ParametersOperation.query.filter_by(id_operations=operation_id).all()
    
    # Добавление новых параметров для новой операции
    for parameter in parameters_operations:
        new_id_parameters = get_new_parameters_operations_id() # Получение нового уникального id параметра
        print(f'new_id_parameters {new_id_parameters}')
        new_id_nomenclature_parameters = parameter.id_nomenclature_parameters
        # cur.execute("""
        #      INSERT INTO parameters_operations (id_parameters, id_operations, id_nomenclature_parameters)
        #     VALUES (%s, %s, %s)
        # """, (new_id_parameters, new_operation_id, new_id_nomenclature_parameters)) 
        new_parameters = ParametersOperation(
            id_parameters = new_id_parameters,
            id_operations=new_operation_id,
            id_nomenclature_parameters = new_id_nomenclature_parameters,
            value = parameter.value
        )
        db.session.add(new_parameters)  # Добавление параметра в сессию
        db.session.commit()  # Сохранение всех изменений
    
    return new_operation_id


def get_new_order_id(cur):
    cur.execute("SELECT COALESCE(MAX(id_order), 0) + 1 FROM orders")
    return cur.fetchone()[0]

def get_new_employee_id(cur):
    cur.execute("SELECT COALESCE(MAX(id_employee), 0) + 1 FROM employee")
    return cur.fetchone()[0]

def get_new_operation_id():
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor() 
    cur.execute("SELECT COALESCE(MAX(id_operations), 0) + 1 FROM operations")
    return cur.fetchone()[0]

def get_new_price_list_id():
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor() 
    cur.execute("SELECT COALESCE(MAX(id_price), 0) + 1 FROM price_list")
    return cur.fetchone()[0]

def get_new_nomenclature_parameters_id():
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()  
    cur.execute("SELECT COALESCE(MAX(id_nomenclature_parameters), 0) + 1 FROM nomenclature_parameters")
    return cur.fetchone()[0]

def get_nomenclature_operations_id():
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()  
    cur.execute("SELECT COALESCE(MAX(id_nomenclature_operation), 0) + 1 FROM nomenclature_operation")
    return cur.fetchone()[0]

def get_materials_id():
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()  
    cur.execute("SELECT COALESCE(MAX(id_materials), 0) + 1 FROM materials")
    return cur.fetchone()[0]

def get_new_nomenclature_orders():
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()  
    cur.execute("SELECT COALESCE(MAX(id_nomenclature_orders), 0) + 1 FROM nomenclature_orders")
    return cur.fetchone()[0]

def get_new_parameters_operations_id():
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()  
    cur.execute("SELECT COALESCE(MAX(id_parameters), 0) + 1 FROM parameters_operations")
    return cur.fetchone()[0]

def get_materials_for_order(order_id):
    print(f'get materials for order')
    try:
        with psycopg2.connect("dbname=Printing user=postgres password=1234") as conn:
            with conn.cursor() as cur:
                # Получаем все операции и их количество для указанного заказа
                cur.execute("""
                    SELECT id_child_operation, quantity_entrance
                    FROM orders
                    WHERE id_order = %s;
                """, (order_id,))
                operations = cur.fetchall()
                #print(operations)
                
                # Список для хранения всех материалов
                all_materials = []

                for operation in operations:
                    # Извлекаем id_child_operation и количество из кортежа
                    #print(f'operation_id {operation[0]}, quantity_entrance {operation[1]}')
                    operation_id = operation[0]
                    quantity_entrance = operation[1]  # Количество

                    # Получаем все материалы для этой операции
                    cur.execute("""
                        SELECT id_materials, number_materials
                        FROM operations
                        WHERE id_operations = %s;
                    """, (operation_id,))
                    materials = cur.fetchall()
                    #print(f'materials {materials}')
                    
                    for material in materials:
                        #print(f'material_id {material[0]}')
                        material_id, number_materials = material
                        if material_id:
                            # Получаем имена и количество материалов
                            cur.execute("""
                                SELECT id_materials, name
                                FROM materials 
                                WHERE id_materials = %s;
                            """, (material_id,))
                            material_info = cur.fetchone() 
                            #print(f'material_info {material_info}')
                            if material_info:
                                # Добавляем информацию о материале и его количестве в общий список
                                all_materials.append({
                                    'id_materials': material_info[0],
                                    'name': material_info[1],
                                    'количество': quantity_entrance * number_materials
                                })
                    #print(f'all_materials {all_materials}')
                return all_materials  
    except Exception as e:
        print(f"Ошибка при получении материалов для заказа: {e}")
        return []  # Возвращаем пустой список при ошибке

def render_materials(order_id):
    print(f'render materials')
    materials = get_materials_for_order(order_id)
    print(f'materials in render_materials {materials}')
    html = ""
    if materials:
        html += "<table>"
        html += "<thead>"
        html += "<tr>"
        html += "<th>Номер материала</th>"
        html += "<th>Название материала</th>"
        html += "<th>Количество</th>"
        html += "</tr>"
        html += "</thead>"
        html += "<tbody>"
        for material in materials:
            html += "<tr>"
            print(f'material {material}')
            # Доступ к элементам словаря по ключам
            html += f"<td>{material['id_materials']}</td>"
            html += f"<td>{material['name']}</td>"
            html += f"<td>{material['количество']}</td>"
            html += "</tr>"
        html += "</tbody>"
        html += "</table>"
    else:
        html += "<p>Нет необходимых материалов для данного заказа.</p>"
    return html

# вывод списка всех заказов
@app.route('/')
@app.route('/index')
def index():   
    session = db.session
    results = (
        session.query(
            Order.id_order,
            Order.status,
            Order.name_orders,
            Order.order_date,
            Employee.id_employee,
            Employee.surname,
            Employee.name_employee,
            Employee.patronymic,
            Employee.position_employee
        )
        .outerjoin(Employee, Order.id_employee == Employee.id_employee)  # Получение информации о сотруднике
        .filter(Order.id_parent_operation == 0)  # Получение всех заказов с родительским ID 0
        .all()
    )

    print(f"Количество заказов: {len(results)}")
    print(f"Результаты запроса: {results}")
    
    session.close()
    return render_template("index.html", results=results)

#вывод заказов со статусом шаблон
@app.route('/template')
def template():
    #фильтрация заказов по статусу и родительскому элементу
    session = db.session
    results = (
        session.query(
            Order.id_order,
            Order.status,
            Order.name_orders,
            Order.order_date,
            Employee.id_employee,
            Employee.surname,
            Employee.name_employee,
            Employee.patronymic,
            Employee.position_employee
        )
        .outerjoin(Employee, Order.id_employee == Employee.id_employee)  # Получение информации о сотруднике
        .filter(Order.id_parent_operation == 0, Order.status == 'шаблон')  # Получение всех заказов с родительским ID 0
        .all()
    )

    print(f"Количество заказов: {len(results)}")
    print(f"Результаты запроса: {results}")
    
    session.close()
    return render_template('template.html', results=results)

#вывод заказов со статусом на удаление
@app.route('/delete')
def delete():
    #фильтрация заказов по статусу и родительскому элементу
    session = db.session
    results = (
        session.query(
            Order.id_order,
            Order.status,
            Order.name_orders,
            Order.order_date,
            Employee.id_employee,
            Employee.surname,
            Employee.name_employee,
            Employee.patronymic,
            Employee.position_employee
        )
        .outerjoin(Employee, Order.id_employee == Employee.id_employee)  # Получение информации о сотруднике
        .filter(Order.id_parent_operation == 0, Order.status == 'удалить')  # Получение всех заказов с родительским ID 0
        .all()
    )

    print(f"Количество заказов: {len(results)}")
    print(f"Результаты запроса: {results}")
    
    session.close()
    return render_template('delete.html', results=results)

#вывод заказов со статусом расчет
@app.route('/calculation')
def calculation():
    #фильтрация заказов по статусу и родительскому элементу
    session = db.session
    results = (
        session.query(
            Order.id_order,
            Order.status,
            Order.name_orders,
            Order.order_date,
            Employee.id_employee,
            Employee.surname,
            Employee.name_employee,
            Employee.patronymic,
            Employee.position_employee
        )
        .outerjoin(Employee, Order.id_employee == Employee.id_employee)  # Получение информации о сотруднике
        .filter(Order.id_parent_operation == 0, Order.status == 'расчет')  # Получение всех заказов с родительским ID 0
        .all()
    )

    print(f"Количество заказов: {len(results)}")
    print(f"Результаты запроса: {results}")
    
    session.close()
    return render_template('calculation.html', results=results)

#вывод заказов со статусом проверен
@app.route('/verified')
def verified():
    #фильтрация заказов по статусу и родительскому элементу
    session = db.session
    results = (
        session.query(
            Order.id_order,
            Order.status,
            Order.name_orders,
            Order.order_date,
            Employee.id_employee,
            Employee.surname,
            Employee.name_employee,
            Employee.patronymic,
            Employee.position_employee
        )
        .outerjoin(Employee, Order.id_employee == Employee.id_employee)  # Получение информации о сотруднике
        .filter(Order.id_parent_operation == 0, Order.status == 'проверен')  # Получение всех заказов с родительским ID 0
        .all()
    )

    print(f"Количество заказов: {len(results)}")
    print(f"Результаты запроса: {results}")
    
    session.close()
    return render_template('verified.html', results=results)

@app.route('/tree/<int:order_id>')  # Определение маршрута для отображения дерева заказов по ID заказа
def tree(order_id):
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")  # Установка соединения с базой данных
    cur = conn.cursor()  # Создание курсора для выполнения запросов
    operations = Operation.query.all()  # Получаем все операции из базы данных
    orders = get_orders(order_id)  # Получаем заказы по заданному ID
    tree = build_tree(orders)  # Строим дерево заказов на основе полученных данных
    circulation = get_circulation(order_id)  # Получаем тираж для заказа
    get_total_cost(order_id)  # Получаем общую стоимость заказа
    material_cost = 0  # Инициализация переменной для стоимости материалов
    operation_cost = 0  # Инициализация переменной для стоимости операций
    # material_cost = calculate_order_amount_material(cur, order_id)  # Расчет стоимости материалов (закомментировано)
    # operation_cost = calculate_order_amount_operation(cur, order_id)  # Расчет стоимости операций (закомментировано)
    total_cost = 0  # Инициализация общей стоимости
    total_cost = float(calculate_order_amount(cur, order_id))  # Расчет общей стоимости заказа    
    # Запрос для получения статуса заказа по его ID
    cur.execute("""
        SELECT status
        FROM orders
        WHERE id_order = %s AND id_parent_operation = 0
    """, (order_id,))  
    status = cur.fetchone()  # Получаем статус заказа
    # Проверка статуса заказа
    if (status[0] == 'расчет' or status[0] == 'на удаление'):
        # Отрисовываем дерево для статуса "расчет"
        tree_html = render_tree(order_id, tree, operations)  
        return render_template('tree_calculation.html', status=status[0], operations=operations, tree_html=tree_html, order_id=order_id, 
                               total_cost=total_cost, circulation=circulation, material_cost=material_cost, operation_cost=operation_cost)
    else:
        # Отрисовываем проверенное дерево для других статусов
        tree_html = render_tree_verified(order_id, tree, operations)  
        return render_template('tree.html', status=status[0], operations=operations, tree_html=tree_html, order_id=order_id, 
                               total_cost=total_cost, circulation=circulation, material_cost=material_cost, operation_cost=operation_cost)

#создание нового заказа
@app.route('/new_order')
def new_order():
    # Получение всех наименований заказов из базы данных
    name_orders = NomenclatureOrders.query.all()
    # Отображение страницы для создания нового заказа с переданными наименованиями
    return render_template("new_order.html", name_orders=name_orders) 

@app.route('/new_order_add', methods=['POST'])
def new_order_add():
    # Получение id выбранного наименования заказа из формы
    id_nomenclature_orders = request.form['name_order']
    # Установка соединения с базой данных
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()  # Создание курсора для выполнения SQL-запросов
    # Получение нового id заказа
    new_order_id = get_new_order_id(cur)
    # Копирование операции (например, создание новой операции на основе шаблона)
    new_operation = copy_operation(1)
    print(f'Новый заказ {new_order_id}')
    print(f'Название заказа {id_nomenclature_orders}')    
    # Запрос для получения названия заказа по его id
    cur.execute("""
        SELECT name_nomenclature_orders
        FROM nomenclature_orders
        WHERE id_nomenclature_orders = %s 
    """, (id_nomenclature_orders,))
    order_data = cur.fetchone()  # Получение данных о заказе    
    # Проверка, существуют ли данные о заказе
    if order_data:
        name_orders = order_data[0]  # Извлечение названия заказа
    else:
        name_orders = 'Заказ'  # Установка значения по умолчанию, если данные не найдены
    print(f'order_data {name_orders}')    
    # Вставка новой записи о заказе в таблицу orders
    cur.execute("""
        INSERT INTO orders (id_order, name_orders, id_parent_operation, id_child_operation, amount, circulation, quantity_entrance, quantity_output, status, number_operations, defective, id_nomenclature_orders)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (new_order_id, name_orders, 0, new_operation, 0, 0, 0, 0, 'расчет', 0, 0, id_nomenclature_orders))    
    conn.commit()  # Подтверждение изменений в базе данных    
    operations = Operation.query.all()  # Получаем все операции
    orders = get_orders(new_order_id)   # Получаем заказы по новому id
    tree = build_tree(orders)  # Строим дерево заказов
    tree_html = render_tree(new_order_id, tree, operations)  # Отрисовываем дерево    
    # Инициализация переменных для расчета стоимости
    total_cost = 0
    material_cost = 0
    operation_cost = 0    
    # Отображение страницы с деревом заказа и его деталями
    return render_template('tree_calculation.html', operations=operations, tree_html=tree_html, order_id=new_order_id, total_cost=total_cost, material_cost=material_cost, operation_cost=operation_cost)

# Получение информации об операции
@app.route('/tree_about_operation/<int:order_id>')
def tree_about_operation(order_id):
    # Установка соединения с базой данных
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()  # Создание курсора для выполнения SQL-запросов
    operations = Operation.query.all()  # Получаем все операции из базы данных
    orders = get_orders(order_id)  # Получаем заказы по заданному ID
    tree = build_tree(orders)  # Строим дерево заказов    
    total_cost = get_total_cost(order_id)  # Получаем общую стоимость заказа
    circulation = get_circulation(order_id)  # Получаем тираж заказа    
    # Запрос для получения статуса заказа по его ID
    cur.execute("""
        SELECT status
        FROM orders
        WHERE id_order = %s AND id_parent_operation = 0
    """, (order_id,))
    status = cur.fetchone()  # Получаем статус заказа    
    # Получаем параметры операции
    cur.execute("""
        SELECT defective_material, defective_percentage
        FROM operations
        WHERE id_operations = 0
    """, ())          
    operation_params = cur.fetchone()  # Получаем параметры операции    
    # Если параметры операции не найдены
    if operation_params is None:
        return jsonify({"success": False, "error": "Параметры операции не найдены."}), 404  # Возвращаем ошибку 404    
    # Извлечение параметров операции
    defective_material, defective_percentage = operation_params
    
    
    
    
    
    # Проверка статуса заказа
    if (status[0] == 'шаблон' or status[0] == 'расчет'):
        tree_html = render_tree(order_id, tree, operations)  # Отрисовываем дерево для статуса "шаблон" или "расчет"
        return render_template('tree_about_operation.html', operations=operations, tree_html=tree_html, order_id=order_id, 
                               total_cost=total_cost, circulation=circulation, defective_material=defective_material, 
                               defective_percentage=defective_percentage)
    else:
        tree_html = render_tree_verified(order_id, tree, operations)  # Отрисовываем проверенное дерево для других статусов
        return render_template('tree_about_operation.html', operations=operations, tree_html=tree_html, order_id=order_id, 
                               total_cost=total_cost, circulation=circulation)  # Отображение страницы с информацией об операции

#добавление операции
@app.route('/add_operation', methods=['POST'])
def add_operation():
    # operation_id = request.form.get('operation_id')
    order_id = request.form.get('order_id')
    parent_id = request.form.get('parent_id')

    # print(f"Received data: operation_id={operation_id}, order_id={order_id}, parent_id={parent_id}")

    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()    

    # new_operation = copy_operation(operation_id)

    # # Вставляем новую операцию в таблицу orders
    # cur.execute("""
    #     INSERT INTO orders (id_order, id_parent_operation, id_child_operation, quantity_entrance, defective, quantity_output, number_operations,amount,circulation)
    #     VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)
    # """, (order_id, parent_id, new_operation,0,0,0,0,0,0))

    # conn.commit()
    operations = Operation.query.filter(Operation.base == True).all()
    
    session = db.session
    results1 = (
    session.query(
        Operation.id_operations, 
        Operation.name_operations,
        TypeWork.name_type_work 
    )
    .join(TypeWork, Operation.id_type_work == TypeWork.id_type_work)
    .filter(Operation.id_operations != 0, Operation.base == True) 
    .group_by(
        Operation.id_operations, 
        Operation.name_operations,
        TypeWork.name_type_work 
    )
    .all()
)


    orders = get_orders(order_id)   # Получаем заказы
    tree = build_tree(orders)       # Строим дерево
    tree_html = render_tree(order_id, tree, operations)  # Отрисовываем дерево
    total_cost = 0
    material_cost = 0
    operation_cost = 0
    cur.execute("""
        SELECT status, circulation
        FROM orders
        WHERE id_order = %s AND id_parent_operation = 0
    """, (order_id,))  
    order_data = cur.fetchone()
    if order_data is not None:
       status, circulation = order_data
    else:
        status =0
        circulation=0 

    return render_template('tree_calculation_add.html', status = status, operations=operations, tree_html=tree_html, order_id=order_id, total_cost=total_cost, 
                           circulation=circulation, material_cost=material_cost,operation_cost=operation_cost, parent_id=parent_id, results1=results1)
    
# Добавление операции
@app.route('/add_operation_new', methods=['POST'])
def add_operation_new():
    print('Добавление операции ')  # Логирование начала процесса добавления операции
    order_id = request.form.get('order_id')  # Получение ID заказа из формы
    operation_id = request.form.get('operation_id')  # Получение ID операции из формы
    parent_id = request.form.get('parent_id')  # Получение ID родительской операции из формы
    # Проверка на заполнение всех обязательных полей
    if not operation_id or not order_id or not parent_id:
        return "All fields are required.", 400  # Возврат ошибки 400, если поля не заполнены
    try:
        # Преобразование полученных данных в целые числа
        operation_id = int(operation_id)
        order_id = int(order_id)
        parent_id = int(parent_id)
    except ValueError:
        return "Invalid input. Please enter valid integers.", 400  # Возврат ошибки 400 при некорректном вводе
    # Установка соединения с базой данных
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()  # Создание курсора для выполнения SQL-запросов
    # Копирование операции на основе переданного id
    new_operation = copy_operation(operation_id)
    # Вставка новой записи о заказе с данными о операции
    cur.execute("""
        INSERT INTO orders (id_order, id_parent_operation, id_child_operation, quantity_entrance, defective, quantity_output, number_operations, amount, circulation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (order_id, parent_id, new_operation, 0, 0, 0, 0, 0, 0))
    conn.commit()  # Подтверждение изменений в базе данных
    operations = Operation.query.all()  # Получение всех операций
    orders = get_orders(order_id)  # Получение заказов по ID
    tree = build_tree(orders)  # Строим дерево заказов
    tree_html = render_tree(order_id, tree, operations)  # Отрисовываем дерево
    total_cost = 0  # Инициализация переменной для общей стоимости
    material_cost = 0  # Инициализация переменной для стоимости материалов
    operation_cost = 0  # Инициализация переменной для стоимости операций
    # Запрос для получения статуса и тиража заказа
    cur.execute("""
        SELECT status, circulation
        FROM orders
        WHERE id_order = %s AND id_parent_operation = 0
    """, (order_id,))    
    order_data = cur.fetchone()  # Получение данных о заказе
    if order_data is not None:
        status, circulation = order_data  # Извлечение статуса и тиража из результата
    else:
        status = 0  # Установка статуса по умолчанию
        circulation = 0  # Установка тиража по умолчанию
    # Отображение страницы с деревом заказа и его деталями
    return render_template('tree_calculation.html', status=status, operations=operations, tree_html=tree_html, order_id=order_id, total_cost=total_cost, 
                           circulation=circulation, material_cost=material_cost, operation_cost=operation_cost)

#удаление заказа
@app.route('/delete_orders', methods=['POST'])
def delete_orders():
    try:
        id_order = request.form.get('id_order')
        conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
        cur = conn.cursor()    
        cur.execute("""
            DELETE FROM orders
                WHERE id_order = %s
        """, (id_order,))
        conn.commit()    
        flash('Заказ успешно удален!', 'success')
        return delete()
    except Exception as e:
        db.session.rollback()  # Откат транзакции в случае ошибки
        flash(f'Ошибка при удалении заказа: {str(e)}', 'danger')

#удаление операции из заказа
@app.route('/delete_operation', methods=['POST'])
def delete_operation():
    operation_id = request.form['operation_id']
    order_id = request.form['order_id']
    parent_id = request.form['parent_id']
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    try:
        # Проверка существования order_id
        cur.execute("SELECT EXISTS(SELECT 1 FROM orders WHERE id_order=%s)", (order_id,))
        order_exists = cur.fetchone()
        order_exists = order_exists[0] if order_exists is not None else False        
        # Проверка существования operation_id
        cur.execute("SELECT EXISTS(SELECT 1 FROM operations WHERE id_operations=%s)", (operation_id,))
        operation_exists = cur.fetchone()
        operation_exists = operation_exists[0] if operation_exists is not None else False
        if not order_exists:
            return jsonify({"success": False, "error": "Указанный order_id не существует."}), 400
        if not operation_exists:
            return jsonify({"success": False, "error": "Указанный operation_id не существует."}), 400     
        cur.execute("""
            DELETE FROM orders 
            WHERE id_order = %s AND id_parent_operation = %s AND id_child_operation = %s
        """, (order_id, parent_id, operation_id))        
        # Получаем все дочерние операции
        cur.execute("""
            SELECT id_parent_operation, id_child_operation
            FROM orders
            WHERE id_parent_operation = %s AND id_order = %s
        """, (operation_id, order_id))  
        child_orders = cur.fetchall()
        # Рекурсивно удаляем дочерние заказы
        for child_order in child_orders:
            parent_order_id = child_order[0]
            child_order_id = child_order[1]
            print(f'Родительская операция ID: {child_order[0]} Дочерняя операция {child_order[1]}')
            delete_child_orders(cur, order_id, parent_order_id, child_order_id)   
        conn.commit()
        operations = Operation.query.all()  # Получаем все операции
        orders = get_orders(order_id)   # Получаем заказы
        if not orders:
            orders = Order.query.filter_by(id_parent_operation=0).all()
            return render_template("index.html", orders=orders)
        else:
            tree = build_tree(orders)       # Строим дерево
            tree_html = render_tree(order_id, tree, operations)  # Отрисовываем дерево
            total_cost = 0
            material_cost = 0
            operation_cost = 0
            return render_template('tree_calculation.html', operations=operations, tree_html=tree_html, order_id=order_id, total_cost=total_cost,material_cost=material_cost,operation_cost=operation_cost)
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

#удаление дочерних операций
def delete_child_orders(cur, order_id, parent_order_id, child_order_id):
    # Выполнение SQL-запроса для удаления дочерней операции из таблицы orders
    cur.execute("""
        DELETE FROM orders 
        WHERE id_order = %s AND id_parent_operation = %s AND id_child_operation = %s
    """, (order_id, parent_order_id, child_order_id))
    # Получаем все дочерние операции
    cur.execute("""
        SELECT id_parent_operation, id_child_operation
        FROM orders
        WHERE id_parent_operation = %s AND id_order = %s
    """, (child_order_id, order_id))  
    child_orders = cur.fetchall()     
    # Рекурсивно удаляем дочерние заказы
    for child_order in child_orders:
        parent_order_id = child_order[0]
        child_order_id = child_order[1]
        # Рекурсивный вызов функции для удаления дочерних операций
        delete_child_orders(cur, order_id, parent_order_id, child_order_id)

#отрисовка дерева со статусом расчет
def render_tree_about_operation(operation_id, order_id, tree, operations, parent=0, visited=None):
    if visited is None:
        visited = set() # Инициализация множества для отслеживания посещенных узлов
    if parent in visited:
        # Проверка на циклические ссылки в дереве
        raise RecursionError(f"Cyclic reference detected at parent: {parent}")
    visited.add(parent) # Добавление текущего узла в посещенные
    html = ""   
    if parent == 0:
        # Получение названия заказа по его id
        order_name = get_order_name_by_id(order_id)
        html += f"<p class='order-info'>Название заказа: {order_name}</p>"
    if parent in tree:
        html += "<ul class='tree'>" # Начало списка для отображения дерева
        for child in tree[parent]:
            #print(f"operation_id {operation_id} child {child['id_child']}")
            if int(operation_id) == int(child['id_child']):     
                #print(f'YES')
                # Добавление информации о дочернем элементе
                html += f"<li><span class='caret text-blue'>{get_quantity_output_operations(child['id_child'], order_id)}шт - {get_name_operations(child['id_child'])} {get_decoding_operations(child['id_child'])}</span>"
            else:
                    # Добавление информации о дочернем элементе
                html += f"<li><span class='caret'>{get_quantity_output_operations(child['id_child'], order_id)}шт - {get_name_operations(child['id_child'])} {get_decoding_operations(child['id_child'])}</span>"
            # Форма для добавления новой операции
            html += f"<form action='{url_for('add_operation')}' method='POST' class='inline-form'>"
            # html += "<select name='operation_id' required class='operation-select'>"
            # for operation in operations:
            #     html += f"<option value='{operation.id_operations}'>ID: {operation.id_operations} - {operation.name_operations}</option>"
            # html += "</select>"
            html += f"<input type='hidden' name='order_id' value='{child['id_order']}'>"
            html += f"<input type='hidden' name='parent_id' value='{child['id_child']}'>"
            # Кнопка для добавления операции
            html += """<button type="submit" class="btn btn-secondary btn-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"></path>
<path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"></path>
</svg>
            </button>"""
            # Форма для удаления операции
            html += "</form>"
            html += f"<form action='{url_for('delete_operation')}' method='POST' class='inline-form'>"
            html += f"<input type='hidden' name='operation_id' value='{child['id_child']}'>"
            html += f"<input type='hidden' name='order_id' value='{child['id_order']}'>"
            html += f"<input type='hidden' name='parent_id' value='{parent}'>"
            # Кнопка для удаления операции
            html += """<button type="submit" class="btn btn-secondary btn-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-circle" viewBox="0 0 16 16">
<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
<path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8"/>
</svg>
            </button>"""
            html += "</form>"
            # Форма для получения информации об операции
            html += "</form>"
            html += f"<form action='{url_for('about_operation', operation_id=child['id_child'])}' method='POST' class='inline-form'>"
            html += f"<input type='hidden' name='operation_id' value='{child['id_child']}'>"
            html += f"<input type='hidden' name='order_id' value='{child['id_order']}'>"
            html += f"<input type='hidden' name='parent_id' value='{parent}'>"
            # Кнопка для получения информации об операции
            html += """<button type="submit" class="btn btn-secondary btn-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bullseye" viewBox="0 0 16 16">
<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
<path d="M8 13A5 5 0 1 1 8 3a5 5 0 0 1 0 10m0 1A6 6 0 1 0 8 2a6 6 0 0 0 0 12"/>
<path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6m0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8"/>
<path d="M9.5 8a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0"/>
</svg>
            </button>"""
            html += "</form>"
            # Рекурсивный вызов для отображения дочерних операций
            html += render_tree_about_operation(operation_id, order_id, tree, operations, child['id_child'], visited)
            html += "</li>"
        html += "</ul>"    
    return html # Возврат сгенерированного HTML-кода

#параметры операции в дереве
@app.route('/about_operation/<int:operation_id>', methods=['GET', 'POST'])
def about_operation(operation_id, parent_id = None, order_id = None):
    print(f'ABOUT OPERATIONS')
    print(f'operation_id {operation_id}')
    print(f'parent_id {parent_id}')
    print(f'order_id {order_id}')
    if request.method == 'POST':
        operation_id = request.form.get('operation_id', operation_id)  # Используем значение из формы, если оно есть
        order_id = request.form.get('order_id', order_id)  # Используем значение из формы, если оно есть
        parent_id = request.form.get('parent_id', parent_id)  # Используем значение из формы, если оно есть
    print(f'operation_id {operation_id} order_id {order_id} parent_id {parent_id}')
    session = db.session
    results = (
        session.query(
            ParametersOperation.id_parameters,
            ParametersOperation.id_operations,
            ParametersOperation.id_nomenclature_parameters,
            ParametersOperation.value,
            NomenclatureParameters.id_nomenclature_parameters,
            NomenclatureParameters.name_parameters
        )
        .join(NomenclatureParameters, ParametersOperation.id_nomenclature_parameters == NomenclatureParameters.id_nomenclature_parameters)  # Убедитесь, что условия соединения корректны
        .filter(ParametersOperation.id_operations == operation_id)
        .all()
    )
    session.close()
    operation_name = Operation.query.filter_by(id_operations=operation_id).first()
    order_select = Order.query.filter_by(id_order = order_id, id_parent_operation = 0).first()
    
    coeffcuttings = CoeffCutting.query.all()
    
    print(f'order_select {order_select}')
    total_cost = 0
    material_cost = 0 
    operation_cost = 0 
    
    materials = Materials.query.all()
    
    if operation_name.id_materials is not None: 
        name_material = Materials.query.filter_by(id_materials=operation_name.id_materials).first()
        if name_material is not None:
            print(name_material.name, name_material.price)  # Предполагается, что у вас есть атрибуты name и price
        else:
            print("Материал не найден.")
    
        # Остальная логика вашего кода...
    else:
        name_material = None    
        price_material = None 
        
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    if operation_name.id_materials is not None: 
        cur.execute("""
            SELECT name, price
            FROM materials
            WHERE id_materials = %s
        """, (operation_name.id_materials,))       
        result = cur.fetchone()
        if result is not None:
            name_material, price = result   
            print(name_material, price)
        cur.execute("""
            SELECT quantity_output
            FROM orders
            WHERE id_order = %s and id_parent_operation = %s and id_child_operation = %s
        """, (order_id, parent_id, operation_id))       
        result = cur.fetchone()
        if result:
            kol_material = result[0]
        else:
            kol_material =0 
        price_material = price * kol_material
    else:
        name_material = None    
        price_material = None 
    
    cur.execute("""
        SELECT name, price
        FROM materials
        WHERE id_materials = %s
    """, (operation_name.id_materials,))       
    result = cur.fetchone()
    # Получаем параметры операции
    cur.execute("""
        SELECT amount
        FROM price_list
        WHERE id_price = %s
    """, (operation_name.id_price,))      
    result = cur.fetchone()
    if result is not None:
        price_operation = result[0]
    else:
        price_operation = None
    
    operations = Operation.query.all()  # Получаем все операции
    parameters_operations = NomenclatureParameters.query.all()
    orders = get_orders(order_id)   # Получаем заказы
    tree = build_tree(orders)       # Строим дерево
    tree_html = render_tree_about_operation(operation_id, order_id, tree, operations)  # Отрисовываем дерево   
    print(f'Статус заказа {order_id} {order_select.status}')
    if order_select.status == 'расчет':
        return render_template('tree_calculation_about_operation.html', operation_name=operation_name, results=results, tree_html=tree_html, order_id=order_id, 
                           operations=operations, operation_id=operation_id, parent_id=parent_id,
                           total_cost=total_cost, material_cost = material_cost, operation_cost=operation_cost,
                           parameters_operations=parameters_operations, materials=materials, 
                           price_operation=price_operation, price_material=price_material, name_material=name_material,
                           coeffcuttings=coeffcuttings)
    else:
        return render_template('tree_about_operation.html', operation_name=operation_name, results=results, tree_html=tree_html, order_id=order_id, 
                           operations=operations, operation_id=operation_id,
                           total_cost=total_cost, material_cost = material_cost, operation_cost=operation_cost,
                           parameters_operations=parameters_operations, materials=materials,
                           price_operation=price_operation, price_material=price_material, name_material=name_material,
                           coeffcuttings=coeffcuttings)

@app.route('/update_parameters/<int:operation_id>', methods=['GET', 'POST'])
def update_parameters(operation_id):
    
    order_id = request.form.get('order_id')
    parent_id = request.form.get('parent_id')
    operation_id_from_form = request.form.get('operation_id')  # Получение operation_id
    print(f'UPDATE')
    print(f'operation_id {operation_id}')
    print(f'parent_id {parent_id}')
    print(f'order_id {order_id}')
    try:
        # Обновление значений параметров
        for param_id in request.form.getlist('id_parameters'):
            new_value = request.form.get(f'value_{param_id}')
            if new_value is not None:  # Проверяем, что новое значение не None
                parameter = ParametersOperation.query.get(param_id)  # Получение параметра по ID
                if parameter:
                    parameter.value = new_value  # Обновление значения
                else:
                    flash(f'Параметр с ID {param_id} не найден.', 'warning')
        db.session.commit()  # Сохранение изменений
        #flash('Параметры успешно обновлены!', 'success')
    except Exception as e:
        db.session.rollback()  # Откат транзакции в случае ошибки
        flash(f'Ошибка при обновлении параметров: {str(e)}', 'danger')

    return about_operation(operation_id, parent_id, order_id)  # Используем operation_id из URL

@app.route('/parameters_add', methods=['GET', 'POST'])
def parameters_add():    
    order_id = request.form.get('id_order')  # Измените на 'id_order'
    parent_id = request.form.get('parent_id')
    operation_id = request.form.get('operation_id')  # Получение operation_id
    id_nomenclature_parameters = request.form.get('nomenclature_id')  # Получение id номенклатуры
    
    parameter_name = request.form.get('new_parameters')
    id_parameters = get_new_parameters_operations_id() 

    print(f'id_parameters {id_parameters}, id_operations {operation_id}, id_nomenclature_parameters {id_nomenclature_parameters}, parameter_name {parameter_name}')

    # Создание нового объекта параметра
    new_parameters = ParametersOperation(
        id_parameters=id_parameters,
        id_operations=operation_id,
        id_nomenclature_parameters=id_nomenclature_parameters
    )
    try:
        db.session.add(new_parameters)
        db.session.commit()
        #flash('Новый параметр успешно создан!', 'success')  # Сообщение об успехе
        
    except Exception as e:
        db.session.rollback()  # Откат транзакции в случае ошибки
        flash(f'Ошибка при создании параметра: {str(e)}', 'danger')
    print(f'ADD')
    print(f'operation_id {operation_id}')
    print(f'parent_id {parent_id}')
    print(f'order_id {order_id}')
    return about_operation(int(operation_id), parent_id, order_id)

@app.route('/passport/<int:order_id>')
def order_details(order_id):
    order = Order.query.filter_by(id_order=order_id, id_parent_operation=0).first_or_404()
    employees = Employee.query.all()
    customers = Customers.query.all()
    return render_template('passport.html', order=order, employees=employees, customers=customers)

@app.route('/passport_template/<int:order_id>')
def order_details_template(order_id):
    order = Order.query.filter_by(id_order=order_id, id_parent_operation=0).first_or_404()
    employees = Employee.query.all()
    customers = Customers.query.all()
    return render_template('passport_template.html', order=order, employees=employees, customers=customers)

@app.route('/passport_verified/<int:order_id>')
def order_details_verified(order_id):
    order = Order.query.filter_by(id_order=order_id, id_parent_operation=0).first_or_404()
    employees = Employee.query.all()
    customers = Customers.query.all()
    return render_template('passport_verified.html', order=order, employees=employees, customers=customers)

@app.route('/passport_delete/<int:order_id>')
def order_details_delete(order_id):
    order = Order.query.filter_by(id_order=order_id, id_parent_operation=0).first_or_404()
    employees = Employee.query.all()
    customers = Customers.query.all()
    return render_template('passport_delete.html', order=order, employees=employees, customers=customers)

@app.route('/materials/<int:order_id>')
def materials(order_id):
    order = Order.query.filter_by(id_order=order_id, id_parent_operation=0).first_or_404()
    html_materials = render_materials(order_id)
    return render_template('materials.html', html_materials = html_materials, order=order)

@app.route('/select_manager')
def select_manager():
    employees = Employee.query.all() 
    orders = Order.query.filter_by(id_parent_operation=0).all()  
    return render_template('select_manager.html', employees=employees, orders=orders)

@app.route('/submit_manager', methods=['POST'])
def submit_manager():
    id_employee = request.form.get('id_employee') 
    id_order = request.form.get('id_order')

    if not id_employee:
        flash('Ошибка: Выберите менеджера.', 'danger')
    else:

        id_order = int(id_order)
        orders_updated = Order.query.filter_by(id_order=id_order, id_parent_operation=0).update(
            {Order.id_employee: id_employee}
        )

        db.session.commit() 

    return order_details(id_order)

@app.route('/submit_manager_template', methods=['POST'])
def submit_manager_template():
    id_employee = request.form.get('id_employee') 
    id_order = request.form.get('id_order')

    if not id_order or not id_order.isdigit():
        return "Ошибка: ID заказа должен быть целым числом.", 400

    id_order = int(id_order)
    orders_updated = Order.query.filter_by(id_order=id_order, id_parent_operation=0).update(
        {Order.id_employee: id_employee}
    )

    db.session.commit() 

    return order_details_template(id_order)

@app.route('/update_customers', methods=['POST'])
def update_customers():
    id_order = request.form.get('id_order')
    id_customers = request.form.get('id_customers')
    # # Проверяем, что id_order является действительным целым числом
    # if not id_order or not id_order.isdigit():
    #     return "Ошибка: ID заказа должен быть целым числом.", 400

    # # Проверяем, что id_customers не пустой
    # if not id_customers or not id_customers.isdigit():
    #     return "Ошибка: ID клиента должен быть целым числом.", 400
    if not id_customers or not id_order:          
        flash('Ошибка: Выберите клиента', 'danger')
    else:
        id_order = int(id_order)
        id_customers = int(id_customers) 
        #Обновляем все заказы с указанным id_order и id_parent_operation = 0
        orders_updated = Order.query.filter_by(id_order=id_order, id_parent_operation=0).update(
            {Order.id_customers: id_customers}
    )
    db.session.commit()

    return order_details(id_order)

@app.route('/update_order_date_time', methods=['POST'])
def update_order_date_time():
    id_order = request.form.get('id_order') 
    order_date = request.form.get('order_date')  
    order_time = request.form.get('order_time') 

    # Проверяем, что id_order является действительным целым числом
    if not id_order or not id_order.isdigit():
        return "Ошибка: ID заказа должен быть целым числом.", 400

    id_order = int(id_order)
    if not order_date or not order_time:
        flash('Ошибка: Дата и время завершения обязательны для заполнения.', 'danger')
    else:

        # Обновляем все заказы с указанным id_order и id_parent_operation = 0
        orders_updated = Order.query.filter_by(id_order=id_order, id_parent_operation=0).update(
            {Order.order_date: order_date}
        )

        # Обновляем все заказы с указанным id_order и id_parent_operation = 0
        orders_updated = Order.query.filter_by(id_order=id_order, id_parent_operation=0).update(
            {Order.order_time: order_time}
        )
        
        db.session.commit()

    return order_details(id_order) 

@app.route('/update_order_date', methods=['POST'])
def update_order_date():
    id_order = request.form.get('id_order') 
    order_date = request.form.get('order_date')     

    id_order = int(id_order)
    
    if not order_date:
        flash('Ошибка: Выберите дату.', 'danger')
    else:
        
        # Обновляем все заказы с указанным id_order и id_parent_operation = 0
        orders_updated = Order.query.filter_by(id_order=id_order, id_parent_operation=0).update(
            {Order.order_date: order_date}
        ) 

        db.session.commit()

    return order_details_template(id_order) 

@app.route('/update_date_time_completion', methods=['POST'])
def update_date_time_completion():
    id_order = request.form.get('id_order')  
    date_completion = request.form.get('date_completion')  
    time_completion = request.form.get('time_completion') 

    # Проверяем, что id_order является действительным целым числом
    if not id_order or not id_order.isdigit():
        return "Ошибка: ID заказа должен быть целым числом.", 400

    id_order = int(id_order)
    if not date_completion or not time_completion:
        flash('Ошибка: Дата и время завершения обязательны для заполнения.', 'danger')
    else:
        # Обновляем все заказы с указанным id_order и id_parent_operation = 0
        orders_updated = Order.query.filter_by(id_order=id_order, id_parent_operation=0).update(
            {Order.date_completion: date_completion}
        )  

        # Обновляем все заказы с указанным id_order и id_parent_operation = 0
        orders_updated = Order.query.filter_by(id_order=id_order, id_parent_operation=0).update(
            {Order.time_completion: time_completion}
        )
        
        db.session.commit()  

    return order_details(id_order)

@app.route('/update_status_template', methods=['POST'])
def update_status_template():
    id_order = request.form.get('id_order')
    print(f'{id_order}')

    # Проверяем, что id_order является действительным целым числом
    if not id_order or not id_order.isdigit():
        return "Ошибка: ID заказа должен быть целым числом.", 400

    id_order = int(id_order)

    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    try:
        # Обновляем статус заказа
        cur.execute("""
            UPDATE orders
            SET status = %s
            WHERE id_order = %s AND id_parent_operation = 0
        """, ('шаблон', id_order))

        # Проверяем, сколько строк было обновлено
        if cur.rowcount == 0:
            return "Ошибка: Заказ не найден или не может быть обновлен.", 404

        conn.commit() 
    except Exception as e:
        conn.rollback() 
        return f"Ошибка при обновлении статуса: {str(e)}", 500
    finally:
        cur.close()
        conn.close()

    return order_details_template(id_order) 

@app.route('/update_status_calculation', methods=['POST'])
def update_status_calculation():
    id_order = request.form.get('id_order')
    print(f'{id_order}')

    # Проверяем, что id_order является действительным целым числом
    if not id_order or not id_order.isdigit():
        return "Ошибка: ID заказа должен быть целым числом.", 400

    id_order = int(id_order)

    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    try:
        # Обновляем статус заказа
        cur.execute("""
            UPDATE orders
            SET status = %s
            WHERE id_order = %s AND id_parent_operation = 0
        """, ('расчет', id_order))

        # Проверяем, сколько строк было обновлено
        if cur.rowcount == 0:
            return "Ошибка: Заказ не найден или не может быть обновлен.", 404

        conn.commit()  
    except Exception as e:
        conn.rollback() 
        return f"Ошибка при обновлении статуса: {str(e)}", 500
    finally:
        cur.close()
        conn.close()

    return order_details(id_order) 

@app.route('/update_status_verified', methods=['POST'])
def update_status_verified():
    id_order = request.form.get('id_order')
    print(f'{id_order}')

    # Проверяем, что id_order является действительным целым числом
    if not id_order or not id_order.isdigit():
        return "Ошибка: ID заказа должен быть целым числом.", 400

    id_order = int(id_order)

    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    try:
        # Обновляем статус заказа
        cur.execute("""
            UPDATE orders
            SET status = %s
            WHERE id_order = %s AND id_parent_operation = 0
        """, ('проверен', id_order))

        # Проверяем, сколько строк было обновлено
        if cur.rowcount == 0:
            return "Ошибка: Заказ не найден или не может быть обновлен.", 404

        conn.commit()  
    except Exception as e:
        conn.rollback() 
        return f"Ошибка при обновлении статуса: {str(e)}", 500
    finally:
        cur.close()
        conn.close()

    return order_details_verified(id_order)

@app.route('/update_status_delete', methods=['POST'])
def update_status_delete():
    id_order = request.form.get('id_order')
    print(f'{id_order}')

    # Проверяем, что id_order является действительным целым числом
    if not id_order or not id_order.isdigit():
        return "Ошибка: ID заказа должен быть целым числом.", 400

    id_order = int(id_order)

    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    try:
        # Обновляем статус заказа
        cur.execute("""
            UPDATE orders
            SET status = %s
            WHERE id_order = %s AND id_parent_operation = 0
        """, ('удалить', id_order))

        # Проверяем, сколько строк было обновлено
        if cur.rowcount == 0:
            return "Ошибка: Заказ не найден или не может быть обновлен.", 404

        conn.commit()  
    except Exception as e:
        conn.rollback() 
        return f"Ошибка при обновлении статуса: {str(e)}", 500
    finally:
        cur.close()
        conn.close()

    return order_details_delete(id_order)

@app.route('/calculate_cost/<int:order_id>', methods=['GET', 'POST'])
def calculate_cost(order_id):  
    if request.method == 'POST':
        circulation = request.form.get('circulation', type=int)
        if circulation is None:
            print("Ошибка: Тираж не был введен.")
            return render_template('tree.html', order_id=order_id, total_cost=total_cost)
        conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
        cur = conn.cursor()
        material_cost=0
        # material_cost = calculate_order_amount_material(cur, order_id)
        print(material_cost)
        operation_cost=0
        # operation_cost = calculate_order_amount_operation(cur, order_id)
        print(operation_cost)
               
        update_order(cur, order_id, circulation)#обновить заказ
        total_cost = calculate_order_amount(cur, order_id)#расчет стоимости заказа
        
        cur.execute("""
            UPDATE orders
            SET amount = %s, circulation = %s
            WHERE id_order = %s AND id_parent_operation = 0
        """, (total_cost, circulation, order_id))
        
        print('cумма заказа обновлена')
        print(f'amount {total_cost}')
        conn.commit()
        print(f"Заказ {order_id} обновлен успешно.")
        status='расчет'
        operations = Operation.query.all()  # Получаем все операции
        orders = get_orders(order_id)   # Получаем заказы
        tree = build_tree(orders)       # Строим дерево
        tree_html = render_tree(order_id, tree, operations)  # Отрисовываем дерево
        total_cost = get_total_cost(order_id) #стоимость    
        circulation = get_circulation(order_id) #тираж
        return render_template('tree.html', status = status, operations=operations, tree_html=tree_html, order_id=order_id, total_cost=total_cost, 
                            circulation=circulation, material_cost=material_cost,operation_cost=operation_cost)
    
@app.route('/copy_order_route', methods=['POST'])
def copy_order_route():
    order_id = request.form['id_order'] 
    result = copy_order(order_id)
    #calculate_cost(result)
    # conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    # cur = conn.cursor()    
    return order_details(result) 

@app.route('/order/<int:order_id>')
def your_order_view(order_id):
    order = Order.query.get(order_id) 
    if not order:
        flash("Заказ не найден.")
        return redirect(url_for('some_other_view')) 
    return render_template('order.html', order=order) 

#таблица технологических операций
@app.route('/operation_table', methods=['GET'])
def operation_table():
    if not current_user.is_authenticated:
        abort(403)
    
    if current_user.position_employee != 'администратор':  
        abort(403)  # Запретить доступ          
    session = db.session
    operations = (
    session.query(
        Operation.id_operations, 
        Operation.name_operations,
        Operation.id_type_work,
        Operation.processing,
        PriceList.amount 
    )
    .join(PriceList, Operation.id_price == PriceList.id_price)
    .filter(Operation.base == True) 
    .all()
)
    #operations = Operation.query.filter_by(base=True).all()  
    return render_template("operation_table.html", operations=operations) 

#создание новой операции
@app.route('/new_operation')
def new_operation():
    # Получение всех наименований заказов из базы данных
    name_orders = NomenclatureOrders.query.all()
    # Отображение страницы для создания нового заказа с переданными наименованиями
    return render_template("new_operation.html", name_orders=name_orders) 
@app.route('/new_operation_add', methods=['GET', 'POST'])
def new_operation_add():
    if request.method == 'POST':
        name = request.form.get('name')
        work_type = request.form.get('work_type')
        processing = request.form.get('processing')
        price = request.form.get('price')
        if work_type == 'Печать':
            id_type_work = 4
        elif work_type == 'Препресс':
            id_type_work = 1
        elif work_type == 'ПослеПечать':
            id_type_work = 2
        else:
            id_type_work = 3
        new_id_operation = get_new_operation_id()
        new_id_price=get_new_price_list_id()
        new_id_nomenclature_operation = get_nomenclature_operations_id()
        print(f'new_id_nomenclature_operation {new_id_nomenclature_operation}')
        # Создание нового объекта стоимости
        new_nomenclature_operation = NomenclatureOperations(
            id_nomenclature_operation=new_id_nomenclature_operation,
            name_nomenclature_operation=name
        )       
        db.session.add(new_nomenclature_operation)
        db.session.commit()
        # Создание нового объекта стоимости
        new_price_list = PriceList(
            id_price=new_id_price,
            id_nomenclature_operation=new_id_nomenclature_operation,
            amount=float(price)
        )       
        db.session.add(new_price_list)
        db.session.commit()
        # Создание нового объекта операции
        new_operation = Operation(
            id_operations = new_id_operation,
            name_operations=name,
            id_type_work=id_type_work,
            processing=processing,
            id_price=new_id_price,
            id_nomenclature_operation = new_id_nomenclature_operation,
            base = True
        )
        db.session.add(new_operation)
        db.session.commit()

        try:
            
            flash('Новая операция успешно создана!', 'success')
            return redirect(url_for('operation_table'))  # Перенаправление на главную страницу
        except Exception as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            flash(f'Ошибка при создании операции: {str(e)}', 'danger')

    return render_template('new_operation.html')  # Отображение формы при GET-запросе

@app.route('/operation_edit/<int:id>', methods=['GET', 'POST'])
def operation_edit(id):
    # Получение всех наименований заказов из базы данных
    #operation = Operation.query.filter_by(id_operations = id).first()
    session = db.session
    operation = (
    session.query(
        Operation.id_operations, 
        Operation.name_operations,
        Operation.id_type_work,
        Operation.processing,
        Operation.id_price,
        PriceList.amount 
    )
    .join(PriceList, Operation.id_price == PriceList.id_price)
    .filter(Operation.id_operations == id) 
    .first()
)
    # Отображение страницы для создания нового заказа с переданными наименованиями
    return render_template("operation_edit.html", operation=operation) 
@app.route('/operation_update', methods=['GET', 'POST'])
def operation_update():
    if request.method == 'POST':
        
        id_operations = request.form.get('id_operations')
        name_operations = request.form.get('name_operations')
        id_type_work = request.form.get('id_type_work')
        
        processing = request.form.get('processing')
        id_price = request.form.get('id_price')
        amount = request.form.get('amount')
        print(f'ID {id_operations} name_operations {name_operations} id_type_work {id_type_work} processing {processing} id_price {id_price} amount {amount}')
        if id_type_work == 'препресс':
            type_work = 1
        elif id_type_work == 'после_печати':
            type_work = 2
        elif id_type_work == 'печать':
            type_work = 4
        else:
            type_work = 3
        print(f'ID {id_operations} name_operations {name_operations} type_work {type_work} processing {processing} id_price {id_price} amount {amount}')
        # Создание нового объекта сотрудника
        conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
        cur = conn.cursor()
        cur.execute("""
            UPDATE operations
            SET name_operations = %s, id_type_work = %s, processing = %s
            WHERE id_operations = %s;
            """, (name_operations, type_work, processing, id_operations))
        conn.commit()
        cur.execute("""
            UPDATE price_list
            SET amount = %s
            WHERE id_price = %s;
            """, (amount, id_price))
        conn.commit()
        flash('Данные операции обновлены', 'success')
        return operation_table()
    return operation_table()  # Отображение формы при GET-запросе

@app.route('/operation_delete/<int:id>', methods=['POST'])
def operation_delete(id):
    # Проверка на наличие связанных заказов
    orders_count = Order.query.filter_by(id_child_operation=id).first()
    if orders_count:
        flash('Нельзя удалить операцию, пока существуют связанные заказы.', 'danger')
        return operation_table()

    # Удаление сотрудника
    operation = Operation.query.get_or_404(id)
    db.session.delete(operation)
    db.session.commit()
    flash('Операция успешно удалена.', 'success')
    return operation_table()

#таблица номенклатуры заказов
@app.route('/nomenclature_orders_table', methods=['GET'])
def nomenclature_orders_table():
    if not current_user.is_authenticated:
        abort(403)
    
    if current_user.position_employee != 'администратор':  
        abort(403)  # Запретить доступ          

    results = NomenclatureOrders.query.all()  
    return render_template("nomenclature_orders_table.html", results=results) 

#создание новой номенклатуры заказа
@app.route('/new_nomenclature_orders')
def new_nomenclature_orders():
    # Получение всех наименований заказов из базы данных
    name_orders = NomenclatureOrders.query.all()
    # Отображение страницы для создания нового заказа с переданными наименованиями
    return render_template("new_nomenclature_orders.html", name_orders=name_orders) 
@app.route('/new_nomenclature_orders_add', methods=['GET', 'POST'])
def new_nomenclature_orders_add():
    if request.method == 'POST':
        # Получение данных из формы
        name = request.form.get('name')
        # Создание нового объекта номенклатуры
        id_nomenclature_orders = get_new_nomenclature_orders()
        new_nomenclature = NomenclatureOrders(id_nomenclature_orders=id_nomenclature_orders, name_nomenclature_orders=name)
        # Сохранение в базе данных
        db.session.add(new_nomenclature)
        db.session.commit()

        flash('Новая номенклатура успешно создана!', 'success')
        return redirect(url_for('new_nomenclature_orders'))

    return render_template('new_nomenclature_orders.html')  # Отображение формы при GET-запросе

@app.route('/nomenclature_orders_edit/<int:id>', methods=['GET', 'POST'])
def nomenclature_orders_edit(id):
    # Получение всех наименований заказов из базы данных
    parameter = NomenclatureOrders.query.filter_by(id_nomenclature_orders = id).first()
    # Отображение страницы для создания нового заказа с переданными наименованиями
    return render_template("nomenclature_orders_edit.html", parameter=parameter) 
@app.route('/nomenclature_orders_update', methods=['GET', 'POST'])
def nomenclature_orders_update():
    if request.method == 'POST':
        id_nomenclature_orders = request.form.get('id_nomenclature_orders')
        name_nomenclature_orders = request.form.get('name_nomenclature_orders')
        print(f"ID: {id_nomenclature_orders}, Name: {name_nomenclature_orders}")
        conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
        cur = conn.cursor()
        cur.execute("""
            UPDATE nomenclature_orders
            SET name_nomenclature_orders = %s
            WHERE id_nomenclature_orders = %s;
            """, (name_nomenclature_orders, id_nomenclature_orders))
        conn.commit()
        flash('Данные номенклатуры обновлены', 'success')
        return nomenclature_orders_table()

    return nomenclature_orders_table()  # Отображение формы при GET-запросе

@app.route('/nomenclature_orders_delete/<int:id>', methods=['POST'])
def nomenclature_orders_delete(id):
    # Проверка на наличие связанных заказов
    orders_count = Order.query.filter_by(id_nomenclature_orders=id).first()
    if orders_count:
        flash('Нельзя удалить номенклатуру продукции, пока существуют связанные заказы.', 'danger')
        return nomenclature_orders_table()

    # Удаление сотрудника
    nomenclature = NomenclatureOrders.query.get_or_404(id)
    db.session.delete(nomenclature)
    db.session.commit()
    flash('Номенклатура продукции успешно удалена.', 'success')
    return nomenclature_orders_table()

#таблица материалов
@app.route('/material_table', methods=['GET'])
def material():
    if not current_user.is_authenticated:
        flash('Ошибка: Доступ запрещен', 'danger')  # Сообщение об ошибке
        abort(403)
    
    if current_user.position_employee != 'администратор':  
        flash('Ошибка: Доступ запрещен', 'danger')  # Сообщение об ошибке
        abort(403)  # Запретить доступ         
        
    materials = Materials.query.all()  
    return render_template("material_table.html", materials=materials) 

#создание нового материала
@app.route('/new_materials')
def new_materials():
    # Получение всех наименований заказов из базы данных
    name_orders = NomenclatureOrders.query.all()
    # Отображение страницы для создания нового заказа с переданными наименованиями
    return render_template("new_materials.html", name_orders=name_orders) 
@app.route('/new_materials_add', methods=['GET', 'POST'])
def new_materials_add():
    if request.method == 'POST':
        # Получение данных из формы
        id_materials = get_materials_id()
        material_name = request.form.get('material_name')
        price = request.form.get('price')
        # Создание нового материала
        new_materials = Materials(id_materials=id_materials, name=material_name, price=price)
        db.session.add(new_materials)
        db.session.commit()

        flash('Новый материал успешно создан!', 'success')  # Сообщение об успехе
        return material()  # Перенаправление на главную страницу

    return render_template('new_materials_add.html')  # Отображение формы при GET-запросе

@app.route('/material_edit/<int:id>', methods=['GET', 'POST'])
def material_edit(id):
    # Получение всех наименований заказов из базы данных
    material = Materials.query.filter_by(id_materials = id).first()
    # Отображение страницы для создания нового заказа с переданными наименованиями
    return render_template("materials_edit.html", material=material) 
@app.route('/material_update', methods=['GET', 'POST'])
def material_update():
    if request.method == 'POST':
        id_materials = request.form.get('id_materials')
        name = request.form.get('name')
        price = request.form.get('price')
        print(f"ID: {id_materials}, Name: {name}, Price: {price}")
        # Создание нового объекта сотрудника
        conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
        cur = conn.cursor()
        cur.execute("""
            UPDATE materials
            SET name = %s, price = %s
            WHERE id_materials = %s;
            """, (name, price, id_materials))
        conn.commit()
        flash('Данные материала обновлены', 'success')
        return material()

    return material()  # Отображение формы при GET-запросе

@app.route('/material_delete/<int:id>', methods=['POST'])
def material_delete(id):
    # Проверка на наличие связанных заказов
    operation = ParametersOperation.query.filter_by(id_materials=id).first()
    if operation:
        flash('Нельзя удалить параметр, пока существуют связанные операции.', 'danger')
        return material()

    # Удаление сотрудника
    material = Materials.query.get_or_404(id)
    db.session.delete(material)
    db.session.commit()
    flash('Материал успешно удален.', 'success')
    return material()

#таблица сотрудников
@app.route('/employee_table', methods=['GET'])
def employee_table():   
    if not current_user.is_authenticated:
        flash('Ошибка: Доступ запрещен', 'danger')  # Сообщение об ошибке
        abort(403)
    
    if current_user.position_employee != 'администратор':  
        flash('Ошибка: Доступ запрещен', 'danger')  # Сообщение об ошибке
        abort(403)  # Запретить доступ       
    employees = Employee.query.all()  
    return render_template("employee_table.html", employees=employees) 

#создание нового сотрудника
@app.route('/new_employee')
def new_employee():
    # Получение всех наименований заказов из базы данных
    employees = Employee.query.all()
    # Отображение страницы для создания нового заказа с переданными наименованиями
    return render_template("new_employee.html", employees=employees) 
@app.route('/new_employee_add', methods=['GET', 'POST'])
def new_employee_add():
    if request.method == 'POST':
        id_employee = request.form.get('id_employee')
        surname = request.form.get('surname')
        name_employee = request.form.get('name_employee')
        patronymic = request.form.get('patronymic')
        position_employee = request.form.get('position_employee')
        password = request.form.get('password')
        
        # Проверка на существование id_employee
        existing_employee = Employee.query.filter_by(id_employee=id_employee).first()
        if existing_employee:
            flash('Сотрудник с таким ID уже существует.', 'danger')
            return redirect(url_for('new_employee_add'))  # Перенаправление на ту же страницу для повторного ввода
        
        # Создание нового объекта сотрудника
        new_employee = Employee(
            id_employee=id_employee,
            surname=surname,
            name_employee=name_employee,
            patronymic=patronymic,
            position_employee=position_employee,
            password=generate_password_hash(password)  # Хеширование пароля
        )
        db.session.add(new_employee)
        db.session.commit()
        flash('Новый сотрудник успешно создан!', 'success')
        return redirect(url_for('index'))

    return render_template('new_employee.html')  # Отображение формы при GET-запросе

@app.route('/employee_edit/<int:id>', methods=['GET', 'POST'])
def employee_edit(id):
    # Получение всех наименований заказов из базы данных
    employee = Employee.query.filter_by(id_employee = id).first()
    # Отображение страницы для создания нового заказа с переданными наименованиями
    return render_template("employee_edit.html", employee=employee) 
@app.route('/employee_update', methods=['GET', 'POST'])
def employee_update():
    if request.method == 'POST':
        id_employee = request.form.get('id_employee')
        surname = request.form.get('surname')
        name_employee = request.form.get('name_employee')
        patronymic = request.form.get('patronymic')
        position_employee = request.form.get('position_employee')
        password = request.form.get('password')
        if password:
            password = generate_password_hash(password)
        
        # Создание нового объекта сотрудника
        conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
        cur = conn.cursor()
        cur.execute("""
            UPDATE employee
            SET surname = %s, name_employee = %s, patronymic = %s, position_employee = %s, password = %s
            WHERE id_employee = %s;
            """, (surname, name_employee, patronymic, position_employee, password, id_employee))
        conn.commit()
        flash('Данные сотрудника обновлены', 'success')
        return employee_table()

    return render_template('employee_edit.html')  # Отображение формы при GET-запросе

@app.route('/employee_delete/<int:id>', methods=['POST'])
def employee_delete(id):
    # Проверка на наличие связанных заказов
    orders_count = Order.query.filter_by(id_employee=id).first()
    if orders_count:
        flash('Нельзя удалить сотрудника, пока существуют связанные заказы.', 'danger')
        return employee_table()

    # Удаление сотрудника
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Сотрудник успешно удален.', 'success')
    return employee_table()

#таблица номенклатуры параметров операции
@app.route('/nomenclature_parameters_table', methods=['GET'])
def nomenclature_parameters_table():
    if not current_user.is_authenticated:
        flash('Ошибка: Доступ запрещен', 'danger')  # Сообщение об ошибке
        abort(403)
    
    if current_user.position_employee != 'администратор':  
        flash('Ошибка: Доступ запрещен', 'danger')  # Сообщение об ошибке
        abort(403)  # Запретить доступ         
        
    nomenclature_parameters = NomenclatureParameters.query.all()  
    return render_template("nomenclature_parameters_table.html", nomenclature_parameters=nomenclature_parameters) 

#создание нового параметра операци
@app.route('/new_nomenclature_parameters')
def new_nomenclature_parameters():
    # Получение всех наименований заказов из базы данных
    nomenclature_parameters = NomenclatureParameters.query.all()  
    # Отображение страницы для создания нового заказа с переданными наименованиями
    return render_template("new_nomenclature_parameters.html", nomenclature_parameters=nomenclature_parameters) 
@app.route('/new_nomenclature_parameters_add', methods=['GET', 'POST'])
def new_nomenclature_parameters_add():
    if request.method == 'POST':
        # Получение данных из формы
        parameter_name = request.form.get('new_parameters')
        id_nomenclature_parameters = get_new_nomenclature_parameters_id()
        # Создание нового материала
        new_parameters = NomenclatureParameters(id_nomenclature_parameters=id_nomenclature_parameters, name_parameters=parameter_name)
        db.session.add(new_parameters)
        db.session.commit()

        flash('Новый материал успешно создан!', 'success')  # Сообщение об успехе
        return redirect(url_for('nomenclature_parameters_table'))  # Перенаправление на главную страницу

    return render_template('new_nomenclature_parameters_add.html')  # Отображение формы при GET-запросе

@app.route('/nomenclature_parameter_edit/<int:id>', methods=['GET', 'POST'])
def nomenclature_parameter_edit(id):
    # Получение всех наименований заказов из базы данных
    parameter = NomenclatureParameters.query.filter_by(id_nomenclature_parameters = id).first()
    # Отображение страницы для создания нового заказа с переданными наименованиями
    return render_template("nomenclature_parameters_edit.html", parameter=parameter) 
@app.route('/nomenclature_parameters_update', methods=['GET', 'POST'])
def nomenclature_parameters_update():
    if request.method == 'POST':
        id_nomenclature_parameters = request.form.get('id_nomenclature_parameters')
        name_parameters = request.form.get('name_parameters')
        
        # Создание нового объекта сотрудника
        conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
        cur = conn.cursor()
        cur.execute("""
            UPDATE nomenclature_parameters
            SET name_parameters = %s
            WHERE id_nomenclature_parameters = %s;
            """, (name_parameters, id_nomenclature_parameters))
        conn.commit()
        flash('Данные параметра обновлены', 'success')
        return nomenclature_parameters_table()

    return nomenclature_parameters_table()  # Отображение формы при GET-запросе

@app.route('/nomenclature_parameters_delete/<int:id>', methods=['POST'])
def nomenclature_parameters_delete(id):
    # Проверка на наличие связанных заказов
    operation = ParametersOperation.query.filter_by(id_nomenclature_parameters=id).first()
    if operation:
        flash('Нельзя удалить параметр, пока существуют связанные операции.', 'danger')
        return nomenclature_parameters_table()

    # Удаление сотрудника
    parameters = NomenclatureParameters.query.get_or_404(id)
    db.session.delete(parameters)
    db.session.commit()
    flash('Параметр успешно удален.', 'success')
    return nomenclature_parameters_table()

#таблица заказов
@app.route('/orders_table', methods=['GET'])
def orders_table():
    order_id = request.args.get('order_id')  # Получаем order_id из параметров запроса
    if order_id:
        orders = Order.query.filter(Order.id_order == order_id).all()  # Фильтрация по id_order
    else:
        orders = Order.query.all()  # Получаем все заказы, если order_id не указан
    
    session = db.session
    results = (
        session.query(
            Order.id_parent_operation,
            Order.id_child_operation,
            Order.amount,
            Order.circulation,
            Order.quantity_entrance,
            Order.number_operations,
            Order.defective,
            Order.quantity_output,
            Order.name_orders,
            Operation.id_operations,
            Operation.name_operations,
            Operation.defective_material,
            Operation.chroma,
            Operation.id_materials,
            Operation.cutting_parts,
            Operation.id_coeff_cutting
        )
        .join(Operation, Order.id_child_operation == Operation.id_operations)
        .filter(Order.id_order == order_id)
        .all()
    )

    session.close()

    print(f"Результаты запроса: {results}")  
    return render_template("orders_table.html", results=results) 

#таблица коэффициентов резки
@app.route('/coeff_cutting_table', methods=['GET'])
def coeff_cutting_table():
    coeffs = CoeffCutting.query.all()  
    return render_template("coeff_cutting_table.html", coeffs=coeffs)

@app.errorhandler(403)
def forbidden(error):
    flash('У вас нет доступа к этой странице.', 'danger')
    return redirect(request.referrer or url_for('index'))  # Возврат на предыдущую страницу или на главную

#авторизация пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        id_employee = form.name_employee.data  # Получаем ID сотрудника       
        if not id_employee.isnumeric():  # Проверяем, является ли id_employee числом
            flash('ID сотрудника должен быть числом', 'danger')
            return redirect(url_for('login'))
        id_employee = int(id_employee)  # Преобразуем в целое число
        password = form.password.data  # Получаем пароль
        # Проверка существования сотрудника с указанным ID
        employee = Employee.query.filter_by(id_employee=id_employee).first()
        if employee:  # Если сотрудник существует
            # Аутентификация сотрудника
            if Employee.authenticate(id_employee, password):
                login_user(employee)
                flash('Успешный вход!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Неверные учетные данные', 'danger')
        else:
            flash('Сотрудник с указанным ID не найден', 'danger')
    else:
        print(form.errors)
    return render_template('login.html', form=form)


#выход сотрудника
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

#изменение материала операции
@app.route('/update_material', methods=['POST'])
def update_material():
    operation_id = request.form['operation_id']
    order_id = request.form['order_id']
    parent_id = request.form.get('parent_id')
    new_material = request.form.get('new_material')
    number_material = request.form.get('number_material')
    if not new_material:
        return "Выберите материал.", 400  # Проверка на случай, если ничего не выбрано
    try:
        conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
        cur = conn.cursor()        
        cur.execute("""
            UPDATE operations
            SET id_materials = %s, number_materials = %s
            WHERE id_operations = %s;
        """, (new_material, number_material, operation_id))        
        conn.commit()
    except Exception as e:
        print(f"Ошибка при обновлении материала: {e}")
        return "Произошла ошибка при обновлении материала.", 500
    finally:
        cur.close()
        conn.close()
    print(f'UPDATE METERIAL')
    print(f'operation_id {operation_id}')
    print(f'parent_id {parent_id}')
    print(f'order_id {order_id}')
    return about_operation(int(operation_id), parent_id, order_id)

#изменение кол-во в одной
@app.route('/update_quantity_in_one', methods=['POST'])
def update_quantity_in_one():
    operation_id = request.form['operation_id']
    order_id = request.form['order_id']
    parent_id = request.form.get('parent_id')
    quantity_in_one = request.form['quantity_in_one']
    
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()        
    cur.execute("""
        UPDATE operations
        SET quantity_in_one = %s
        WHERE id_operations = %s;
    """, (quantity_in_one, operation_id))   
    conn.commit()
    cur.close()
    conn.close()
    
    print(f'update_quantity_in_one')
    print(f'operation_id {operation_id}')
    print(f'parent_id {parent_id}')
    print(f'order_id {order_id}')
    print(f'quantity_in_one {quantity_in_one}')
    return about_operation(int(operation_id), parent_id, order_id)

#изменение цветности операции
@app.route('/update_chroma', methods=['POST'])
def update_chroma():
    operation_id = request.form['operation_id']
    order_id = request.form['order_id']
    new_chroma = request.form['new_chroma']
    try:
        result = eval(new_chroma)
        number_colors = int(result)
    except ValueError as e:
        print("Ошибка преобразования:", e)
    except Exception as e:
        print("Ошибка:", e)
    #result = copy_operation(operation_id) #копирование операции, новый id операции
    print(f'новая цветность {update_chroma}')
    print(f'новая операция {operation_id}')
    
    if new_chroma is None:
        new_chroma = None
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    cur.execute("""
        UPDATE operations
        SET chroma = %s, number_colors = %s
        WHERE id_operations = %s;
    """, (new_chroma, number_colors, operation_id))              
        
    # Получаем все дочерние операции
    cur.execute("""
        SELECT id_parent_operation, id_child_operation
        FROM orders
        WHERE id_parent_operation = %s AND id_order = %s
    """, (operation_id, order_id))  
    child_orders = cur.fetchall()

    # Рекурсивно обновляем дочерние заказы
    for child_order in child_orders:
        parent_order_id = child_order[0]
        child_order_id = child_order[1]
        update_chroma_child(cur, order_id, parent_order_id, child_order_id, new_chroma, number_colors)    
    conn.commit()      
    return tree(order_id) 

#изменение цветности дочерних операций
def update_chroma_child(cur, order_id, parent_order_id, child_order_id, new_chroma, number_colors):
    cur.execute("""
        UPDATE operations
        SET chroma = %s, number_colors = %s
        WHERE id_operations = %s;
    """, (new_chroma, number_colors, child_order_id))              
        
    # Получаем все дочерние операции
    cur.execute("""
        SELECT id_parent_operation, id_child_operation
        FROM orders
        WHERE id_parent_operation = %s AND id_order = %s
    """, (child_order_id, order_id))  
    child_orders = cur.fetchall()

    # Рекурсивно обновляем дочерние заказы
    for child_order in child_orders:
        parent_order_id = child_order[0]
        child_order_id = child_order[1]
        update_chroma_child(cur, order_id, parent_order_id, child_order_id, new_chroma, number_colors)
       
#изменение расшифровки операции
@app.route('/update_decoding', methods=['POST'])
def update_decoding():
    operation_id = request.form.get('operation_id')
    order_id = request.form.get('order_id')
    parent_id = request.form.get('parent_id')
    decoding = request.form.get('decoding')
    print(f'новая расшифровка {decoding}')
    print(f'номер закааз {order_id}')
    print(f'новая операция {operation_id}')
    
    if decoding is None:
        decoding = None
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    cur.execute("""
        UPDATE operations
        SET decoding = %s
        WHERE id_operations = %s;
    """, (decoding, operation_id))              
        
    # Получаем все дочерние операции
    cur.execute("""
        SELECT id_parent_operation, id_child_operation
        FROM orders
        WHERE id_parent_operation = %s AND id_order = %s
    """, (operation_id, order_id))  
    child_orders = cur.fetchall()

    # Рекурсивно обновляем дочерние заказы
    for child_order in child_orders:
        parent_order_id = child_order[0]
        child_order_id = child_order[1]
        update_decoding_child(cur, order_id, parent_order_id, child_order_id, decoding)    
    conn.commit()      
    return about_operation(operation_id, parent_id, order_id)

#изменение цветности дочерних операций
def update_decoding_child(cur, order_id, parent_order_id, child_order_id, decoding):
    print(f'child_id {child_order_id}')
    cur.execute("""
        UPDATE operations
        SET decoding = %s
        WHERE id_operations = %s;
    """, (decoding, child_order_id))              
        
    # Получаем все дочерние операции
    cur.execute("""
        SELECT id_parent_operation, id_child_operation
        FROM orders
        WHERE id_parent_operation = %s AND id_order = %s
    """, (child_order_id, order_id))  
    child_orders = cur.fetchall()

    # Рекурсивно обновляем дочерние заказы
    for child_order in child_orders:
        parent_order_id = child_order[0]
        child_order_id = child_order[1]
        update_decoding_child(cur, order_id, parent_order_id, child_order_id, decoding)       
        
#изменить брак в штуках
@app.route('/update_defective_material', methods=['POST'])
def update_defective_material():
    operation_id = request.form['operation_id']
    order_id = request.form['order_id']
    parent_id = request.form['parent_id']
    defective_material = request.form.get('new_defective_material')
    #result = copy_operation(operation_id)
    print(f'новый ьрак в штуках {defective_material}')
    print(f'новая операция {operation_id}')
    
    if defective_material is None:
        defective_material = None
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    cur.execute("""
            UPDATE operations
            SET defective_material = %s
            WHERE id_operations = %s;
        """, (defective_material, operation_id))  
    
    # cur.execute("""
    #         UPDATE orders
    #         SET id_child_operation = %s
    #         WHERE id_order = %s AND id_parent_operation = %s AND id_child_operation = %s;
    #     """, (operation_id, order_id, parent_id, operation_id))  
    
    # Получаем все дочерние операции
    # cur.execute("""
    #     SELECT id_child_operation
    #     FROM orders
    #     WHERE id_parent_operation = %s AND id_order = %s
    # """, (operation_id, order_id))  
    # child_orders = cur.fetchall()

    # # Рекурсивно обновляем дочерние заказы
    # for child_order in child_orders:
    #     child_order_id = child_order[0]   
    #     print(f'result {result}')
    #     print(f'order_id {order_id}')
    #     print(f'parent_id {operation_id}')
    #     print(f'дочерний элемент {child_order_id}') 
    #     #обновление дочерние операции заказа
    #     cur.execute("""
    #             UPDATE orders
    #             SET id_parent_operation = %s
    #             WHERE id_order = %s AND id_parent_operation = %s AND id_child_operation = %s;
    #         """, (result, order_id, operation_id, child_order_id)) 
    
    conn.commit()  

    return tree(order_id) 

#изменить брак в процентах
@app.route('/update_defective_percentage', methods=['POST'])
def update_defective_percentage():
    operation_id = request.form['operation_id']
    order_id = request.form['order_id']
    parent_id = request.form['parent_id']
    defective_percentage = request.form.get('new_defective_percentage')
    #result = copy_operation(operation_id)
    print(f'новый ьрак в штуках {defective_percentage}')
    print(f'новая операция {operation_id}')
    
    if defective_percentage is None:
        defective_percentage = None
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    cur.execute("""
            UPDATE operations
            SET defective_percentage = %s
            WHERE id_operations = %s;
        """, (defective_percentage, operation_id))  
    
    # cur.execute("""
    #         UPDATE orders
    #         SET id_child_operation = %s
    #         WHERE id_order = %s AND id_parent_operation = %s AND id_child_operation = %s;
    #     """, (result, order_id, parent_id, operation_id))  
    
    # # Получаем все дочерние операции
    # cur.execute("""
    #     SELECT id_child_operation
    #     FROM orders
    #     WHERE id_parent_operation = %s AND id_order = %s
    # """, (operation_id, order_id))  
    # child_orders = cur.fetchall()

    # # Рекурсивно обновляем дочерние заказы
    # for child_order in child_orders:
    #     child_order_id = child_order[0]   
    #     print(f'result {result}')
    #     print(f'order_id {order_id}')
    #     print(f'parent_id {operation_id}')
    #     print(f'дочерний элемент {child_order_id}') 
    #     #обновление дочерние операции заказа
    #     cur.execute("""
    #             UPDATE orders
    #             SET id_parent_operation = %s
    #             WHERE id_order = %s AND id_parent_operation = %s AND id_child_operation = %s;
    #         """, (result, order_id, operation_id, child_order_id)) 
    
    conn.commit()  

    return tree(order_id) 

#изменить кол-во частей для резки
@app.route('/update_cutting_parts', methods=['GET','POST'])
def update_cutting_parts():
    operation_id = request.form['operation_id']
    order_id = request.form['order_id']
    parent_id = request.form['parent_id']
    new_cutting_parts = request.form.get('new_cutting_parts')
    #result = copy_operation(operation_id)
    print(f'новая резка {new_cutting_parts}')
    print(f'новая операция {operation_id}')
    
    if new_cutting_parts is None:
        new_cutting_parts = None
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()
    cur.execute("""
            UPDATE operations
            SET cutting_parts = %s
            WHERE id_operations = %s;
        """, (new_cutting_parts, operation_id))  
    
    # cur.execute("""
    #         UPDATE orders
    #         SET id_child_operation = %s
    #         WHERE id_order = %s AND id_parent_operation = %s AND id_child_operation = %s;
    #     """, (result, order_id, parent_id, operation_id))  
    
    # # Получаем все дочерние операции
    # cur.execute("""
    #     SELECT id_child_operation
    #     FROM orders
    #     WHERE id_parent_operation = %s AND id_order = %s
    # """, (operation_id, order_id))  
    # child_orders = cur.fetchall()

    # # Рекурсивно обновляем дочерние заказы
    # for child_order in child_orders:
    #     child_order_id = child_order[0]   
    #     print(f'result {result}')
    #     print(f'order_id {order_id}')
    #     print(f'parent_id {operation_id}')
    #     print(f'дочерний элемент {child_order_id}') 
    #     #обновление дочерние операции заказа
    #     cur.execute("""
    #             UPDATE orders
    #             SET id_parent_operation = %s
    #             WHERE id_order = %s AND id_parent_operation = %s AND id_child_operation = %s;
    #         """, (result, order_id, operation_id, child_order_id))     
    conn.commit()  

    return tree(order_id) 

#изменить коэффициент резки
@app.route('/update_coeff_cutting', methods=['GET', 'POST'])
def update_coeff_cutting():
    cutting_coefficient_id = request.form.get('cutting_coefficient')
    order_id = request.form.get('id_order')
    operation_id = request.form.get('operation_id')
    parent_id = request.form.get('parent_id')

    # Обработка обновления коэффициента
    try:
        # Найдите коэффициент по ID
        coefficient = CoeffCutting.query.get(cutting_coefficient_id)
        if coefficient:
            operation = Operation.query.get(operation_id)
            if operation:
                operation.id_coeff_cutting = coefficient.id_coeff_cutting 
                db.session.commit()  # Сохраните изменения
                flash('Коэффициент для резки успешно обновлён!', 'success')
            else:
                flash('Операция не найдена.', 'danger')
        else:
            flash('Коэффициент не найден.', 'danger')
    except Exception as e:
        db.session.rollback()  # Откат транзакции в случае ошибки
        flash(f'Ошибка при обновлении коэффициента: {str(e)}', 'danger')

    return about_operation(operation_id, parent_id, order_id)


@app.route('/generate_pdf/<int:order_id>')
def generate_pdf(order_id):
    conn = psycopg2.connect("dbname=Printing user=postgres password=1234")
    cur = conn.cursor()

    operations = Operation.query.all()  # Получаем все операции
    orders = get_orders(order_id)   # Получаем заказы
    tree = build_tree(orders)       # Строим дерево     
    circulation = get_circulation(order_id) #тираж 
    total_cost = get_total_cost(order_id) #стоимостьm
    material_cost = 0
    operation_cost = 0
    
    session = db.session
    results1 = (
    session.query(
        Order.id_child_operation,        
        Operation.name_operations,
        Order.quantity_output,
        Order.quantity_entrance,
        Order.defective,
        Operation.id_type_work,
        NomenclatureParameters.name_parameters,        
        ParametersOperation.value
    )
    .join(Operation, Order.id_child_operation == Operation.id_operations)
    .join(ParametersOperation, Operation.id_operations == ParametersOperation.id_operations)
    .join(NomenclatureParameters, NomenclatureParameters.id_nomenclature_parameters == ParametersOperation.id_nomenclature_parameters)
    .filter(Order.id_order == order_id, Operation.id_type_work == 1) #препресс
    .all()
    )

    print(f"Результаты запроса ДоПечать: {results1}")
    
    # Группируем результаты по id_child_operation
    grouped_results_1 = {}
    for operation in results1:
        if operation.id_child_operation not in grouped_results_1:
            grouped_results_1[operation.id_child_operation] = {
                "name_operations": operation.name_operations,
                "quantity_output": operation.quantity_output,
                "quantity_entrance": operation.quantity_entrance,
                "defective": operation.defective,
                "parameters": []
            }
        grouped_results_1[operation.id_child_operation]["parameters"].append({
            "name_parameters": operation.name_parameters,
            "value": operation.value
        }) 
    
    session = db.session
    results2 = (
    session.query(
        Order.id_child_operation,        
        Operation.name_operations,
        Order.quantity_output,
        Order.quantity_entrance,
        Order.defective,
        Operation.id_type_work,
        NomenclatureParameters.name_parameters,        
        ParametersOperation.value
    )
    .join(Operation, Order.id_child_operation == Operation.id_operations)
    .join(ParametersOperation, Operation.id_operations == ParametersOperation.id_operations)
    .join(NomenclatureParameters, NomenclatureParameters.id_nomenclature_parameters == ParametersOperation.id_nomenclature_parameters)
    .filter(Order.id_order == order_id, Operation.id_type_work == 2) #послепечать
    .all()
    )

    print(f"Результаты запроса ДоПечать: {results2}")
    
    # Группируем результаты по id_child_operation
    grouped_results_2 = {}
    for operation in results2:
        if operation.id_child_operation not in grouped_results_2:
            grouped_results_2[operation.id_child_operation] = {
                "name_operations": operation.name_operations,
                "quantity_output": operation.quantity_output,
                "quantity_entrance": operation.quantity_entrance,
                "defective": operation.defective,
                "parameters": []
            }
        grouped_results_2[operation.id_child_operation]["parameters"].append({
            "name_parameters": operation.name_parameters,
            "value": operation.value
        }) 
    
    session = db.session
    results3 = (
    session.query(
        Order.id_child_operation,        
        Operation.name_operations,
        Order.quantity_output,
        Order.quantity_entrance,
        Order.defective,
        Operation.id_type_work,
        NomenclatureParameters.name_parameters,        
        ParametersOperation.value
    )
    .join(Operation, Order.id_child_operation == Operation.id_operations)
    .join(ParametersOperation, Operation.id_operations == ParametersOperation.id_operations)
    .join(NomenclatureParameters, NomenclatureParameters.id_nomenclature_parameters == ParametersOperation.id_nomenclature_parameters)
    .filter(Order.id_order == order_id, Operation.id_type_work == 3) #допечать
    .all()
    )

    print(f"Результаты запроса ДоПечать: {results3}")
    
    # Группируем результаты по id_child_operation
    grouped_results_3 = {}
    for operation in results3:
        if operation.id_child_operation not in grouped_results_3:
            grouped_results_3[operation.id_child_operation] = {
                "name_operations": operation.name_operations,
                "quantity_output": operation.quantity_output,
                "quantity_entrance": operation.quantity_entrance,
                "defective": operation.defective,
                "parameters": []
            }
        grouped_results_3[operation.id_child_operation]["parameters"].append({
            "name_parameters": operation.name_parameters,
            "value": operation.value
        })   
        
    session = db.session
    results4 = (
    session.query(
        Order.id_child_operation,        
        Operation.name_operations,
        Order.quantity_output,
        Order.quantity_entrance,
        Order.defective,
        Operation.id_type_work,
        NomenclatureParameters.name_parameters,        
        ParametersOperation.value
    )
    .join(Operation, Order.id_child_operation == Operation.id_operations)
    .join(ParametersOperation, Operation.id_operations == ParametersOperation.id_operations)
    .join(NomenclatureParameters, NomenclatureParameters.id_nomenclature_parameters == ParametersOperation.id_nomenclature_parameters)
    .filter(Order.id_order == order_id, Operation.id_type_work == 4) #печать
    .all()
    )

    print(f"Результаты запроса ДоПечать: {results4}")
    
    # Группируем результаты по id_child_operation
    grouped_results_4 = {}
    for operation in results4:
        if operation.id_child_operation not in grouped_results_4:
            grouped_results_4[operation.id_child_operation] = {
                "name_operations": operation.name_operations,
                "quantity_output": operation.quantity_output,
                "quantity_entrance": operation.quantity_entrance,
                "defective": operation.defective,
                "parameters": []
            }
        grouped_results_4[operation.id_child_operation]["parameters"].append({
            "name_parameters": operation.name_parameters,
            "value": operation.value
        })  

    tree_html = render_tree_pdf(order_id, tree, operations)  # Отрисовываем дерево 
      
    return render_template('generate_pdf.html', tree_html=tree_html, order_id=order_id, results1=results1, results2=results2, results3=results3, results4=results4,
                               total_cost=total_cost, circulation=circulation,  material_cost=material_cost, operation_cost=operation_cost,
                               grouped_results_3=grouped_results_3, grouped_results_2=grouped_results_2,
                                grouped_results_1=grouped_results_1, grouped_results_4=grouped_results_4)

if __name__ == '__main__':
    app.run(debug='0.0.0.0')


