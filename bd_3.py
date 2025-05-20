import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE equipment (
            id_equipment SERIAL PRIMARY KEY,
            name_equipment VARCHAR(100) NOT NULL,
            status VARCHAR(100)
        );
        '''
        
        cursor.execute(create_table_query)
        
        connection.commit()  # Подтверждение изменений
        print('Таблица equipment создана')
    
    except Exception as e:
        print("Ошибка при создании таблицы:", e)
    
    finally:
        # Закрытие курсора и подключения
        cursor.close()
        connection.close()

# Вызов функции
create_table()
