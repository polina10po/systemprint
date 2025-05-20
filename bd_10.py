import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE orders
        (            
            id_order integer NOT NULL,
            name_orders text COLLATE pg_catalog."default",
            id_parent_operation integer NOT NULL,
            id_child_operation integer NOT NULL,
            amount real,
            circulation integer,
            quantity_entrance integer,
            number_operations integer,
            defective integer,
            quantity_output integer,
            status text COLLATE pg_catalog."default",
            id_customers integer,
            order_date date,
            order_time time without time zone,
            date_completion date,
            time_completion time without time zone,
            id_employee integer,
            id_nomenclature_orders integer,
            quantity_in_one real,
            CONSTRAINT orders_pkey PRIMARY KEY (id_order, id_parent_operation, id_child_operation),
            CONSTRAINT orders_id_child_operation_fkey FOREIGN KEY (id_child_operation)
                REFERENCES public.operations (id_operations) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID,
            CONSTRAINT orders_id_customers_fkey FOREIGN KEY (id_customers)
                REFERENCES public.customers (id_customer) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID,
            CONSTRAINT orders_id_employee_fkey FOREIGN KEY (id_employee)
                REFERENCES public.employee (id_employee) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID,
            CONSTRAINT orders_id_nomenclature_orders_fkey FOREIGN KEY (id_nomenclature_orders)
                REFERENCES public.nomenclature_orders (id_nomenclature_orders) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID,
            CONSTRAINT orders_id_parent_operation_fkey FOREIGN KEY (id_parent_operation)
                REFERENCES public.operations (id_operations) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID
        );
        '''
        
        cursor.execute(create_table_query)
        print('Таблица orders создана')
        
        # SQL-запрос для вставки значений
        insert_query = '''
        INSERT INTO orders (id_order, name_orders, id_parent_operation, id_child_operation, amount, circulation, quantity_entrance, number_operations, defective, quantity_output, status,  id_nomenclature_orders, quantity_in_one)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        
        # Вставка нескольких записей
        values_to_insert = [
            (1, 'Буклет А4, 1 фальц', 0, 1,   13293.78, 100,  100, 100, 0,   100, 'шаблон', 1, 1),
            (1, 'Буклет А4, 1 фальц', 1, 2,   None,     None, 100, 100, 0,   100, 'шаблон', 1, 1),
            (1, 'Буклет А4, 1 фальц', 2, 3,   None,     None, 100, 100, 0,   100, 'шаблон', 1, 1),
            (1, 'Буклет А4, 1 фальц', 3, 4,   None,     None, 111, 100, 11,  100, 'шаблон', 1, 1),
            (1, 'Буклет А4, 1 фальц', 4, 5,   None,     None, 31,  28,  3,   111, 'шаблон', 1, 1),
            (1, 'Буклет А4, 1 фальц', 5, 6,   None,     None, 31,  31,  0,   31,  'шаблон', 1, 1),
            (1, 'Буклет А4, 1 фальц', 6, 7,   None,     None, 352, 31,  321, 31,  'шаблон', 1, 1),
            (1, 'Буклет А4, 1 фальц', 7, 8,   None,     None, 8,   8,   0,   8,   'шаблон', 1, 1),
            (1, 'Буклет А4, 1 фальц', 7, 11,  None,     None, 177, 176, 1,   352, 'шаблон', 1, 1),
            (1, 'Буклет А4, 1 фальц', 8, 9,   None,     None, 8,   8,   0,   8,   'шаблон', 1, 1),
            (1, 'Буклет А4, 1 фальц', 9, 10,  None,     None, 8,   8,   0,   8,   'шаблон', 1, 1)
        ]
        
        # Выполнение вставки всех записей за один раз
        cursor.executemany(insert_query, values_to_insert)        
        connection.commit()  # Подтверждение изменений
        print('Данные в orders вставлены')
    
    except Exception as e:
        print("Ошибка при создании таблицы:", e)
    
    finally:
        # Закрытие курсора и подключения
        cursor.close()
        connection.close()

# Вызов функции
create_table()
