import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE type_work
        (            
            id_type_work SERIAL PRIMARY KEY,
            name_type_work VARCHAR(100) NOT NULL
        );
        '''
        
        cursor.execute(create_table_query)
        print('Таблица nomenclature_operations создана')
        
        # SQL-запрос для вставки значений
        insert_query = '''
        INSERT INTO type_work (id_type_work, name_type_work)
        VALUES (%s, %s);
        '''
        
        # Вставка нескольких записей
        values_to_insert = [
            (1, 'Препресс'),
            (2, 'ПослеПечать'),
            (3, 'ДоПечать'),
            (4, 'Печать')
            
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
