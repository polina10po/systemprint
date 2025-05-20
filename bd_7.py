import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE nomenclature_orders
        (            
            id_nomenclature_orders SERIAL PRIMARY KEY,
            name_nomenclature_orders VARCHAR(100) NOT NULL
        );
        '''
        
        cursor.execute(create_table_query)
        print('Таблица nomenclature_orders создана')
        
        # SQL-запрос для вставки значений
        insert_query = '''
        INSERT INTO nomenclature_orders (id_nomenclature_orders, name_nomenclature_orders)
        VALUES (%s, %s);
        '''
        
        # Вставка нескольких записей
        values_to_insert = [
            (1, 'Буклет А4, 1 фальц'),
            (2, 'Визитка 4+4')
            
        ]
        
        # Выполнение вставки всех записей за один раз
        cursor.executemany(insert_query, values_to_insert)        
        connection.commit()  # Подтверждение изменений
        print('Данные в nomenclature_orders вставлены')
    
    except Exception as e:
        print("Ошибка при создании таблицы:", e)
    
    finally:
        # Закрытие курсора и подключения
        cursor.close()
        connection.close()

# Вызов функции
create_table()
