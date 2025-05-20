import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE materials
        (            
            id_materials SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price REAL
        );
        '''
        
        cursor.execute(create_table_query)
        print('Таблица materials создана')
        
        # SQL-запрос для вставки значений
        insert_query = '''
        INSERT INTO materials (id_materials, name, price)
        VALUES (%s, %s, %s);
        '''
        
        # Вставка нескольких записей
        values_to_insert = [
            (1, 'Пластина офсетная SM74 605х745х0,3', 133.34),
            (2, 'Бумага GALERIE ART GLOSS 115гр 620х940', 4),
            (3, 'Картон GRAPHIART DUO 285гр 72х102 +', 13.92),
            
        ]
        
        # Выполнение вставки всех записей за один раз
        cursor.executemany(insert_query, values_to_insert)        
        connection.commit()  # Подтверждение изменений
        print('Данные в materials вставлены')
    
    except Exception as e:
        print("Ошибка при создании таблицы:", e)
    
    finally:
        # Закрытие курсора и подключения
        cursor.close()
        connection.close()

# Вызов функции
create_table()
