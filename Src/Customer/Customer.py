import re

class Customer: #create an empty customer for system with attributes all set to None to avoid AttributeError
    def __init__(self, first_name, last_name, address, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone_number = phone_number


    #Verify methods to check value passes in correctly
    @staticmethod
    def verify_first_name( first_name):
        return isinstance(first_name, str) and len(first_name) > 0
    @staticmethod
    def verify_last_name( last_name):
        return isinstance(last_name, str) and len(last_name) > 0
    @staticmethod
    def verify_address( address):
        return isinstance(address, str) and len(address) > 0
    @staticmethod
    def verify_phone_number( phone_number):
        return isinstance(phone_number, str) and  re.fullmatch(r"[0-9]{10}", phone_number) is not None

    #create customer when validation is complete
    #every field is checked, if any field fails nothing will be created
    #if nothing fails new customer is created


class CustomerManager:
    def __init__(self):
        self.customers = {}
        self.next_id = 1

    def create_customer(self, first_name, last_name, address, phone_number):
        if not (Customer.verify_first_name(first_name)
            and Customer.verify_last_name(last_name)
            and Customer.verify_address(address)
            and Customer.verify_phone_number(phone_number)):
            return False
        else:
            customer = Customer(first_name, last_name, address, phone_number)
            customer_id = self.next_id
            self.customers[customer_id] = customer
            self.next_id += 1
            return customer_id

    def read_customer(self, customer_id):
        if customer_id in self.customers:
            return self.customers[customer_id]

    def read_all_customers(self):
        return dict(self.customers)

    def update_customer(self, customer_id, first_name, last_name, address, phone_number):
        customer = self.read_customer(customer_id)
        if customer is None:
            return False

        if not(Customer.verify_first_name(first_name)
            and Customer.verify_last_name(last_name)
            and Customer.verify_address(address)
            and Customer.verify_phone_number(phone_number)):
            return False

        customer.first_name = first_name
        customer.last_name = last_name
        customer.address = address
        customer.phone_number = phone_number
        return True

    def delete_customer(self, customer_id):
        if customer_id in self.customers:
            del self.customers[customer_id]
            return True
        else:
            return False
