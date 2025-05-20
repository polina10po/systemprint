import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()
        
        # SQL-запрос для создания таблицы
        create_table_query = '''
        CREATE TABLE employee (
            id_employee integer NOT NULL,
            surname character varying(255) COLLATE pg_catalog."default" NOT NULL,
            name_employee character varying(255) COLLATE pg_catalog."default" NOT NULL,
            patronymic character varying(255) COLLATE pg_catalog."default",
            position_employee character varying(255) COLLATE pg_catalog."default" NOT NULL,
            id_equipment integer,
            password character varying(255) COLLATE pg_catalog."default",
            CONSTRAINT employee_pkey PRIMARY KEY (id_employee),
            CONSTRAINT employee_id_equipment_fkey FOREIGN KEY (id_equipment)
            REFERENCES public.equipment (id_equipment) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
        );
        '''
        
        cursor.execute(create_table_query)
        connection.commit()  # Подтверждение изменений
        print('Таблица employee создана')
        
        # SQL-запрос для вставки значений
        insert_query = '''
        INSERT INTO employee (id_employee, surname, name_employee, patronymic, position_employee, password)
        VALUES (%s, %s, %s, %s, %s, %s);
        '''
    
        hashed_password = generate_password_hash('12345678')
        
        # Вставка нескольких записей
        values_to_insert = [
            (1, 'Иванов', 'Иван', 'Иванович', 'менеджер', hashed_password),
            (2, 'Петров', 'Петр', 'Петрович', 'менеджер', hashed_password),
            (3, 'Сидоров', 'Олег', 'Николаевич', 'администратор', hashed_password),
            (4, 'Смирнов', 'Александр', 'Дмитриевич', 'менеджер', hashed_password),
            (5, 'Кузнецов', 'Дмитрий', 'Николаевич', 'администратор', hashed_password)
            
        ]
        
        # Выполнение вставки всех записей за один раз
        cursor.executemany(insert_query, values_to_insert)        
        connection.commit()  # Подтверждение изменений
        print('Данные в employee вставлены')
    
    except Exception as e:
        print("Ошибка при создании таблицы:", e)
    
    finally:
        # Закрытие курсора и подключения
        cursor.close()
        connection.close()

# Вызов функции
create_table()
