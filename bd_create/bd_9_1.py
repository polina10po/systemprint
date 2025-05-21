import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE nomenclature_parameters
        (            
            id_nomenclature_parameters integer NOT NULL,
            name_parameters VARCHAR(100),
            CONSTRAINT nomenclature_parameters_pkey PRIMARY KEY (id_nomenclature_parameters)
        );
        '''
        
        cursor.execute(create_table_query)
        print('Таблица parameters_operations создана')
        
        # SQL-запрос для вставки значений
        insert_query = '''
        INSERT INTO nomenclature_parameters (
            id_nomenclature_parameters, name_parameters)
	        VALUES (%s, %s);
        '''
        
        # Вставка нескольких записей
        values_to_insert = [
            (1, 'Брак, штуки'),
            (2, 'Брак, проценты'),
            (3, 'Цветность'),
            (4, 'Раскроить на кол-во частей')
        ]
        
        # Выполнение вставки всех записей за один раз
        cursor.executemany(insert_query, values_to_insert)        
        connection.commit()  # Подтверждение изменений
        print('Данные в operatparameters_operationsions вставлены')
    
    except Exception as e:
        print("Ошибка при создании таблицы:", e)
    
    finally:
        # Закрытие курсора и подключения
        cursor.close()
        connection.close()

# Вызов функции
create_table()
