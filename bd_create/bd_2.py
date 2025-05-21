import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE coeff_cutting (
            id_coeff_cutting SERIAL PRIMARY KEY,
            name_coeff_cutting VARCHAR(100) NOT NULL,
            coeff_cutting FLOAT NOT NULL
        );
        '''
        
        cursor.execute(create_table_query)
        print('Таблица coeff_cutting создана')
        
        # SQL-запрос для вставки значений
        insert_query = '''
        INSERT INTO coeff_cutting (name_coeff_cutting, coeff_cutting)
        VALUES (%s, %s);
        '''
        
        # Вставка нескольких записей
        values_to_insert = [
            ('Меловка 80-90гр', 1.3),
            ('Меловка 115-130гр', 1.3),
            ('Меловка 150-170', 1.6),
            ('Меловка 200-250', 2),
            ('Самоклейка', 2.8),
            ('Самокопирка', 1.5),
            ('Меловка 300гр', 2.5),
            ('Мелованный картон', 2.5)
            
        ]
        
        # Выполнение вставки всех записей за один раз
        cursor.executemany(insert_query, values_to_insert)        
        connection.commit()  # Подтверждение изменений
        print('Данные добавлены в таблицу coeff_cutting')
    
    except Exception as e:
        print("Ошибка при создании таблицы:", e)
    
    finally:
        # Закрытие курсора и подключения
        cursor.close()
        connection.close()

# Вызов функции
create_table()
