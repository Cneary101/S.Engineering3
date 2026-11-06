# Records the bill for one customer and month.
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

    # Check the customer/bill ID and the billing month.
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

    # Charge only for deliveries completed in the selected month.
    def calculate_total(self, deliveries, customerId, month):
        total = 0

        for delivery in deliveries:
            if delivery['customer_id'] == customerId and delivery['delivered']:
                if delivery['date'].startswith(month):
                    total = total + delivery['price'] * delivery['quantity']

        return round(total, 2)

    # Validate inputs before calculating the final total.
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


# Keeps bills together until the database/DAO is connected.
class BillManager:
    def __init__(self):
        self.bills = {}

    def create_bill(self, billId, customerId, month, deliveries):
        if billId in self.bills:
            return False

        bill = Bill()
        if not bill.create_bill(billId, customerId, month, deliveries):
            return False

        self.bills[billId] = bill
        return billId

    def read_bill(self, billId):
        return self.bills.get(billId)

    def read_all_bills(self):
        return dict(self.bills)

    def update_bill(self, billId, customerId, month, deliveries):
        bill = self.read_bill(billId)
        if bill is None:
            return False

        # Recalculate if changes are made
        if not bill.verify_id(customerId) or not bill.verify_month(month):
            return False
        if not isinstance(deliveries, list):
            return False

        bill.customerId = customerId
        bill.month = month
        bill.total = bill.calculate_total(deliveries, customerId, month)
        return True

    def delete_bill(self, billId):
        # Removes a draft bill
        if billId not in self.bills:
            return False

        del self.bills[billId]
        return True
