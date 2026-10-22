class Delivery_Person:
    def __init__(self, driver_id, name):
        self.driver_id = driver_id
        self.name = name

    def get_name(self):
        return self.name

    def get_id(self):
        return self.driver_id

    #Verify that the name of the Delivery person is valid
    #The name must be a string that contains only letters and spaces(it will not accept apostrophes)
    #It returns True if it is valid and False otherwise
    def verifyName(self):
        if not isinstance(self.name, str) or not self.name.strip():
            return False
        return all(part.isalpha() for part in self.name.split())

    #Since the id will be the primary key in the database this ensures that it is an int and that it is unique, therefore we dont need a verifyID() method
