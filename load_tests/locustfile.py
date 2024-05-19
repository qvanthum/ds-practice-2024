from locust import HttpUser, TaskSet, task, between

class OrderExecutionTasks(TaskSet):

    @task
    def single_non_fraudulent_order(self):
        """Simulate a single non-fraudulent order"""
        order_data = {
            "orderId": "order1",
            "userData": {
                "name": "Alice",
                "address": "123 Main St"
            },
            "creditCard": {
                "number": "4111111111111111",
                "expiry": "12/25",
                "cvv": "456"
            },
            "items": [
                {"name": "Book A", "quantity": 1}
            ]
        }
        self.client.post("/order", json=order_data)

    @task
    def multiple_non_fraudulent_orders(self):
        """Simulate multiple non-fraudulent orders"""
        orders = [
            {
                "orderId": "order2",
                "userData": {
                    "name": "Bob",
                    "address": "456 Market St"
                },
                "creditCard": {
                    "number": "4111111111111111",
                    "expiry": "12/25",
                    "cvv": "456"
                },
                "items": [
                    {"name": "Book B", "quantity": 2}
                ]
            },
            {
                "orderId": "order3",
                "userData": {
                    "name": "Charlie",
                    "address": "789 Elm St"
                },
                "creditCard": {
                    "number": "4111111111111111",
                    "expiry": "12/25",
                    "cvv": "456"
                },
                "items": [
                    {"name": "Book C", "quantity": 3}
                ]
            }
        ]
        for order in orders:
            self.client.post("/order", json=order)

    @task
    def mixed_orders(self):
        """Simulate mixed orders with both fraudulent and non-fraudulent orders"""
        orders = [
            {
                "orderId": "order4",
                "userData": {
                    "name": "James",  # Fraudulent user
                    "address": "101 Maple St"
                },
                "creditCard": {
                    "number": "4111111111111111",
                    "expiry": "12/25",
                    "cvv": "456"
                },
                "items": [
                    {"name": "Book D", "quantity": 1}
                ]
            },
            {
                "orderId": "order5",
                "userData": {
                    "name": "Eve",
                    "address": "202 Oak St"
                },
                "creditCard": {
                    "number": "4111111111111111",
                    "expiry": "12/25",
                    "cvv": "123"  # Fraudulent CVV
                },
                "items": [
                    {"name": "Book E", "quantity": 1}
                ]
            }
        ]
        for order in orders:
            self.client.post("/order", json=order)

    @task
    def conflicting_orders(self):
        """Simulate conflicting orders attempting to purchase the same book"""
        orders = [
            {
                "orderId": "order6",
                "userData": {
                    "name": "Frank",
                    "address": "303 Pine St"
                },
                "creditCard": {
                    "number": "4111111111111111",
                    "expiry": "12/25",
                    "cvv": "456"
                },
                "items": [
                    {"name": "Book F", "quantity": 1}
                ]
            },
            {
                "orderId": "order7",
                "userData": {
                    "name": "Grace",
                    "address": "404 Birch St"
                },
                "creditCard": {
                    "number": "4111111111111111",
                    "expiry": "12/25",
                    "cvv": "456"
                },
                "items": [
                    {"name": "Book F", "quantity": 1}
                ]
            }
        ]
        for order in orders:
            self.client.post("/order", json=order)


class WebsiteUser(HttpUser):
    tasks = [OrderExecutionTasks]
    wait_time = between(1, 5)

