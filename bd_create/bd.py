import psycopg2

def create_table():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect("dbname=Printing user=postgres password=1234")
        
        cursor = connection.cursor()

        # SQL-запрос для удаления таблицы
        drop_query = "DROP TABLE IF EXISTS orders CASCADE;"  # Удаляем таблицу только если она существует
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица orders удалена')
        
        # SQL-запрос для удаления таблицы
        drop_query = "DROP TABLE IF EXISTS operations CASCADE;"  # Удаляем таблицу только если она существует
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица operations удалена')
        
        drop_query = "DROP TABLE IF EXISTS nomenclature_operation CASCADE;"  # Удаляем таблицу только если она существует
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица nomenclature_operation удалена')

        drop_query = "DROP TABLE IF EXISTS nomenclature_parameters CASCADE;"  # Удаляем таблицу только если она существует
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица nomenclature_parameters удалена')

        drop_query = "DROP TABLE IF EXISTS parameters_operations CASCADE;"  # Удаляем таблицу только если она существует
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица parameters_operations удалена')

        # SQL-запрос для удаления таблицы
        drop_query = "DROP TABLE IF EXISTS type_work;"  # Удаляем таблицу только если она существует
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица type_work удалена')
        
        # SQL-запрос для удаления таблицы
        drop_query = "DROP TABLE IF EXISTS nomenclature_orders;"  # Удаляем таблицу только если она существует        
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица nomenclature_orders удалена')
        
        # SQL-запрос для удаления таблицы
        drop_query = "DROP TABLE IF EXISTS price_list;"  # Удаляем таблицу только если она существует        
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица price_list удалена')
        
         # SQL-запрос для удаления таблицы
        drop_query = "DROP TABLE IF EXISTS nomenclature_operation;"  # Удаляем таблицу только если она существует        
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица nomenclature_operation удалена')   
        
        # SQL-запрос для удаления таблицы
        drop_query = "DROP TABLE IF EXISTS materials;"  # Удаляем таблицу только если она существует        
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица materials удалена')
        
        # SQL-запрос для удаления таблицы
        drop_query = "DROP TABLE IF EXISTS customers;"  # Удаляем таблицу только если она существует        
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица customers удалена')
        
        # SQL-запрос для удаления таблицы
        drop_query = "DROP TABLE IF EXISTS coeff_cutting;"  # Удаляем таблицу только если она существует        
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица coeff_cutting удалена')
        
        # SQL-запрос для удаления таблицы
        drop_query = "DROP TABLE IF EXISTS employee;"  # Удаляем таблицу только если она существует        
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица employee удалена')
        
        # SQL-запрос для удаления таблицы
        drop_query = "DROP TABLE IF EXISTS equipment;"  # Удаляем таблицу только если она существует        
        cursor.execute(drop_query)  # Выполняем запрос
        print('Таблица equipment удалена')
        
        # # # SQL-запрос для создания таблицы
        # create_table_query = '''
        # CREATE TABLE coeff_cutting (
        #     id_coeff_cutting SERIAL PRIMARY KEY,
        #     name_coeff_cutting VARCHAR(100) NOT NULL,
        #     coeff_cutting FLOAT NOT NULL
        # );
        # '''
        
        # cursor.execute(create_table_query)
        
        # # SQL-запрос для вставки значений
        # insert_query = '''
        # INSERT INTO coeff_cutting (name_coeff_cutting, coeff_cutting)
        # VALUES (%s, %s);
        # '''
        
        # # Вставка нескольких записей
        # values_to_insert = [
        #     ('Меловка 80-90гр', 1.3),
        #     ('Меловка 115-130гр', 1.3),
        #     ('Меловка 150-170', 1.6),
        #     ('Меловка 200-250', 2),
        #     ('Самоклейка', 2.8),
        #     ('Самокопирка', 1.5),
        #     ('Меловка 300гр', 2.5),
        #     ('Мелованный картон', 2.5)
            
        # ]
        
        # # Выполнение вставки всех записей за один раз
        # cursor.executemany(insert_query, values_to_insert)
        
        connection.commit()  # Подтверждение изменений
    
    except Exception as e:
        print("Ошибка при создании таблицы:", e)
    
    finally:
        # Закрытие курсора и подключения
        cursor.close()
        connection.close()

# Вызов функции
create_table()
