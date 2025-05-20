import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE nomenclature_operation
        (            
            id_nomenclature_operation SERIAL PRIMARY KEY,
            name_nomenclature_operation VARCHAR(100) NOT NULL
        );
        '''
        
        cursor.execute(create_table_query)
        print('Таблица nomenclature_operations создана')
        
        # SQL-запрос для вставки значений
        insert_query = '''
        INSERT INTO nomenclature_operation (id_nomenclature_operation, name_nomenclature_operation)
        VALUES (%s, %s);
        '''
        
        # Вставка нескольких записей
        values_to_insert = [
            (1, 'Доставка продукции'),
            (2, 'Доработка макета'),
            (3, 'Упаковка'),
            (4, 'Фальцовка автоматическая'),
            (5, 'Резка'),
            (6, 'Контроль'),
            (7, 'Офсет на PM-74'),
            (8, 'Засветка печатных форм'),
            (9, 'Фотовывод'),
            (10, 'Монтаж ПЛ офсет')
            
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
