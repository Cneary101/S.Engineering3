class Bill:
    def __init__(self):
        self.billId = None
        self.customerId = None
        self.month = None
        self.total = None

    def getBillId(self):
        return self.billId

    def getCustomerId(self):
        return self.customerId

    def getMonth(self):
        return self.month

    def getTotal(self):
        return self.total

    def verify_id(self, value):
        return type(value) is int and value > 0

    def verify_month(self, month):
        if not isinstance(month, str):
            return False

        parts = month.split('-')
        if len(parts) != 2:
            return False

        year = parts[0]
        number = parts[1]

        if len(year) != 4 or len(number) != 2:
            return False
        if not year.isdigit() or not number.isdigit():
            return False

        return 1 <= int(number) <= 12

    def calculate_total(self, deliveries, customerId, month):
        total = 0

        for delivery in deliveries:
            if delivery['customer_id'] == customerId and delivery['delivered']:
                if delivery['date'].startswith(month):
                    total = total + delivery['price'] * delivery['quantity']

        return round(total, 2)

    def create_bill(self, billId, customerId, month, deliveries):
        if not self.verify_id(billId) or not self.verify_id(customerId):
            return False
        if not self.verify_month(month) or not isinstance(deliveries, list):
            return False

        self.billId = billId
        self.customerId = customerId
        self.month = month
        self.total = self.calculate_total(deliveries, customerId, month)
        return True
