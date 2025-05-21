import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE price_list
        (            
            id_price integer NOT NULL,
            circulation_from integer,
            circulation_up integer,
            amount real,
            date date,
            id_nomenclature_operation integer,
            CONSTRAINT price_list_pkey PRIMARY KEY (id_price),
            CONSTRAINT price_list_id_nomenclature_operation_fkey FOREIGN KEY (id_nomenclature_operation)
                REFERENCES public.nomenclature_operation (id_nomenclature_operation) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID
        );
        '''
        
        cursor.execute(create_table_query)
        print('Таблица price_list создана')
        
        # SQL-запрос для вставки значений
        insert_query = '''
        INSERT INTO price_list (id_price, circulation_from, circulation_up, amount, id_nomenclature_operation)
	    VALUES (%s, %s, %s, %s, %s);
        '''
        
        # Вставка нескольких записей
        values_to_insert = [
            (1, 0, 1000, 500, 1),
            (2, 0, 1000, 550, 2),
            (3, 0, 1000, 0, 3),
            (4, 0, 1000, 1000, 4),
            (5, 0, 1000, 323.24, 5),
            (6, 0, 1000, 0, 6),
            (7, 0, 1000, 7149.45, 7),
            (8, 0, 1000, 768, 8),
            (9, 0, 1000, 667.46, 9),
            (10, 0, 1000, 520.25, 10),
            (11, 0, 1000, 40.66, 5),
            (12, 0, 1000, 4738.8, 7),
            (13, 0, 1000, 768, 8),
            (14, 0, 1000, 1952.56, 9),
            (15, 0, 1000, 1040.5, 10),
            (16, 0, 1000, 19.03, 5),
            (17, 0, 1000, 1.57, 5),
            (18, 0, 1000, 0.72, 5)
            
            
        ]
        
        # Выполнение вставки всех записей за один раз
        cursor.executemany(insert_query, values_to_insert)        
        connection.commit()  # Подтверждение изменений
        print('Данные в price_list вставлены')
    
    except Exception as e:
        print("Ошибка при создании таблицы:", e)
    
    finally:
        # Закрытие курсора и подключения
        cursor.close()
        connection.close()

# Вызов функции
create_table()
