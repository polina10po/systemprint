import psycopg2
import random

def generate_phone_number():
    # Генерация номера телефона в формате +7 (XXX) XXX-XX-XX
    area_code = random.randint(100, 999)  # Код города
    first_part = random.randint(100, 999)  # Первая часть номера
    second_part = random.randint(10, 99)    # Вторая часть номера
    third_part = random.randint(10, 99)     # Третья часть номера
    
    phone_number = f"+7 ({area_code}) {first_part}-{second_part}-{third_part}"
    return phone_number

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE customers
        (            
            id_customer SERIAL PRIMARY KEY,
            name_customer VARCHAR(100) NOT NULL,
            contacts VARCHAR(100),
            address VARCHAR(100)
        );
        '''
        
        cursor.execute(create_table_query)
        print('Таблица customers создана')
        
        # SQL-запрос для вставки значений
        insert_query = '''
        INSERT INTO customers (id_customer, name_customer, contacts, address)
        VALUES (%s, %s, %s, %s);
        '''
        
        # Вставка нескольких записей
        values_to_insert = [
            (1, 'Иванов', generate_phone_number(), 'г. Екатеринбург, ул. Мира, 5'),
            (2, 'Петров', generate_phone_number(), 'г. Екатеринбург, ул. Гагарина, 8'),
            (3, 'Сидоров', generate_phone_number(), 'г. Екатеринбург, ул. Пушкина, 137')
            
        ]
        
        # Выполнение вставки всех записей за один раз
        cursor.executemany(insert_query, values_to_insert)        
        connection.commit()  # Подтверждение изменений
        print('Данные в employee вставлены')
    
    except Exception as e:
        print("Ошибка при создании таблицы:", e)
    
    finally:
        # Закрытие курсора и подключения
        cursor.close()
        connection.close()

# Вызов функции
create_table()
