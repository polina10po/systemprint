import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # # SQL-запрос для создания таблицы
        create_table_query = '''
        ALTER TABLE operations
        ADD COLUMN decoding TEXT;
        '''
        
        cursor.execute(create_table_query)
        print('Таблица operations изменена')
    
    except Exception as e:
        print("Ошибка при создании таблицы:", e)
    
    finally:
        # Закрытие курсора и подключения
        cursor.close()
        connection.close()

# Вызов функции
create_table()
