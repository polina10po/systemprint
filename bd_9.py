import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE operations
        (            
            id_operations integer NOT NULL,
            name_operations text COLLATE pg_catalog."default",
            id_materials integer,
            number_materials real,
            id_type_work integer,
            id_coeff_cutting integer,
            id_nomenclature_operation integer,
            id_price integer,
            base boolean,
            lead_time time with time zone,
            id_equipment integer,
            quantity_in_one real,
            processing text COLLATE pg_catalog."default",
            CONSTRAINT "Operations_pkey" PRIMARY KEY (id_operations),
            CONSTRAINT "Operations_ID_Materials_fkey" FOREIGN KEY (id_materials)
                REFERENCES public.materials (id_materials) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            CONSTRAINT operations_id_coeff_cutting_fkey FOREIGN KEY (id_coeff_cutting)
                REFERENCES public.coeff_cutting (id_coeff_cutting) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            CONSTRAINT operations_id_equipment_fkey FOREIGN KEY (id_equipment)
                REFERENCES public.equipment (id_equipment) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            CONSTRAINT operations_id_nomenclature_operation_fkey FOREIGN KEY (id_nomenclature_operation)
                REFERENCES public.nomenclature_operation (id_nomenclature_operation) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            CONSTRAINT operations_id_price_fkey FOREIGN KEY (id_price)
                REFERENCES public.price_list (id_price) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            CONSTRAINT operations_id_type_work_fkey FOREIGN KEY (id_type_work)
                REFERENCES public.type_work (id_type_work) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
        );
        '''
        
        cursor.execute(create_table_query)
        print('Таблица operations создана')
        
        # SQL-запрос для вставки значений
        insert_query = '''
        INSERT INTO operations (id_operations, name_operations, 
        id_materials, number_materials, id_type_work, id_coeff_cutting, 
        id_nomenclature_operation, id_price, base, processing, quantity_in_one)
	    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        
        # Вставка нескольких записей
        values_to_insert = [
            (0, 'Родительская операция заказа', None, None, 2, None, None, 6, None, 'Стандарт', 1),
            (1, 'Доставка продукции',           None, None, 2, None, 1,    1, True, 'Стандарт', 1),
            (2, 'Доработка макета',             None, None, 2, None, 1,    2, True, 'Стандарт', 1),
            (3, 'Упаковка',                     None, None, 2, None, 3,    3, True, 'Стандарт', 1),
            (4, 'Фальцовка автоматическая',     None, None, 2, None, 4,    4, None, 'Стандарт', 1),
            (5, 'Резка',                        None, None, 2, 2,    5,    5, True, 'Резка', 1),                       
            (6, 'Контроль',                     None, None, 2, None, 6,    6, True, 'Стандарт', 1),
            (7, 'Офсет на PM-74',               None, None, 4, None, 7,    7, True, 'Печать', 1),
            (8, 'Засветка печатных форм',       1,    1,    3, None, 8,    8, True, 'Фотовывод', 1),
            (9, 'Фотовывод',                    None, None, 1, None, 9,    9, True, 'Фотовывод', 1),
            (10, 'Монтаж ПЛ офсет',             None, None, 1, None, 10,  10, True, 'Фотовывод', 1),
            (11, 'Резка',                       2,    1,    3, 2,    5,   11, True, 'Резка', 1)
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
