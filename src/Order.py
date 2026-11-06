class Order:
    def __init__(self, customer_id, publication_id, delivery_days):
        self.customer_id = customer_id
        self.publication_id = publication_id
        self.delivery_days = delivery_days.copy()
        self.active = True

    @staticmethod
    def verify_id(value):
        return type(value) is int and value > 0

    @staticmethod
    def verify_delivery_days(days):
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday"]

        if not isinstance(days, list) or len(days) == 0:
            return False

        for day in days:
            if day not in weekdays or days.count(day) > 1:
                return False

        return True


class OrderManager:
    def __init__(self, customers, publications):
        self.customers = customers
        self.publications = publications
        self.orders = {}
        self.next_id = 1

    def verify_publication(self, publication_id):
        return (Order.verify_id(publication_id)
                and publication_id in self.publications
                and self.publications[publication_id].getActive())

    def create_order(self, customer_id, publication_id, delivery_days):
        if not Order.verify_id(customer_id):
            return False

        if self.customers.read_customer(customer_id) is None:
            return False

        if not self.verify_publication(publication_id):
            return False

        if not Order.verify_delivery_days(delivery_days):
            return False

        order_id = self.next_id
        self.orders[order_id] = Order(
            customer_id, publication_id, delivery_days
        )
        self.next_id += 1
        return order_id

    def read_order(self, order_id):
        if not Order.verify_id(order_id):
            return None

        return self.orders.get(order_id)

    def read_all_orders(self):
        return dict(self.orders)

    def update_order(self, order_id, publication_id, delivery_days):
        order = self.read_order(order_id)

        if order is None or not order.active:
            return False

        if not self.verify_publication(publication_id):
            return False

        if not Order.verify_delivery_days(delivery_days):
            return False

        order.publication_id = publication_id
        order.delivery_days = delivery_days.copy()
        return True

    def delete_order(self, order_id):
        order = self.read_order(order_id)

        if order is None or not order.active:
            return False

        # Cancel the order and keep its record.
        order.active = False
        return True
