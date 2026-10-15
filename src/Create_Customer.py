import re

class Create_Customer: #create an empty customer for system with attributes all set to None to avoid AttributeError
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.address = None
        self.phone_number = None

    #Verify methods to check value passes in correctly

    def verify_first_name( first_name):
        return isinstance(first_name, str) and len(first_name) > 0

    def verify_last_name( last_name):
        return isinstance(last_name, str) and len(last_name) > 0

    def verify_address( address):
        return isinstance(address, str) and len(address) > 0

    def verify_phone_number( phone_number):
        return isinstance(phone_number, str) and  re.fullmatch(r"[0-9]{10}", phone_number) is not None

    #create customer when validation is complete
    #every field is checked, if any field fails nothing will be created
    #if nothing fails new customer is created
    def create_customer(self, first_name, last_name, address, phone_number):
        if not (self.verify_first_name(first_name)
            and self.verify_last_name(last_name)
            and self.verify_address(address)
            and self.verify_phone_number(phone_number)):
            return False
        else:
            self.first_name = first_name
            self.last_name = last_name
            self.address = address
            self.phone_number = phone_number
            return True
