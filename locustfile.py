from locust import HttpUser, task, between
import random
from datetime import datetime, timedelta

class OrderUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def copy_order(self):
        order_id = random.randint(1, 2)  # диапозон заказов для копирования
        self.client.post("/copy_order_route", data={"id_order": order_id})

    @task
    def calculate_cost(self):
        order_id = random.randint(1, 40)  # диапазон заказов для расчета стоимости
        circulation = 100  
        self.client.post(f"/calculate_cost/{order_id}", data={"circulation": circulation})

    @task
    def update_date_completion(self):
        order_id = random.randint(1, 40)  # диапазон заказов для изменения даты заказа
        # Генерируем случайную дату завершения
        date_completion = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        self.client.post("/update_date_completion", data={"id_order": order_id, "date_completion": date_completion})
   
