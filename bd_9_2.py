import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE parameters_operations
        (            
            id_parameters integer NOT NULL,
            id_operations integer,
            id_nomenclature_parameters integer,
            value text COLLATE pg_catalog."default",
            CONSTRAINT parameters_operations_pkey PRIMARY KEY (id_parameters),
            CONSTRAINT parameters_operations_id_nomenclature_operations_fkey FOREIGN KEY (id_nomenclature_parameters)
                REFERENCES public.nomenclature_parameters (id_nomenclature_parameters) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            CONSTRAINT parameters_operations_id_operation_fkey FOREIGN KEY (id_operations)
                REFERENCES public.operations (id_operations) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
        );
        '''
        
        cursor.execute(create_table_query)
        print('Таблица parameters_operations создана')
        
        # SQL-запрос для вставки значений
        insert_query = '''
        INSERT INTO parameters_operations (
            id_parameters, id_operations, id_nomenclature_parameters, value)
	        VALUES (%s, %s, %s, %s);
        '''
        
        # Вставка нескольких записей
        values_to_insert = [
            (1, 4,1,'10'),
            (2,4,2,'1'),
            (3,5,1,'2'),
            (4,5,2,'1'),
            (5,5,4,'4'),
            (6,7,3,'4+4'),
            (7,7,2,'1'),
            (8,7,1,'40'),
            (9,8,3,'4+4'),
            (10,9,3,'4+4'),
            (11,10,3,'4+4'),
            (12,11,1,'1'),
            (13,11,4,'2')
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
