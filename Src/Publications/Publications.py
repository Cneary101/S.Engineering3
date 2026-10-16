class Publication:
    def __init__(self, publicationId, name, publicationType, price, quantity, frequency, active=True):
        self.publicationId = publicationId
        self.name = name
        self.publicationType = publicationType
        self.price = price
        self.quantity = quantity
        self.frequency = frequency
        self.active = active

    def getPublicationId(self):
        return self.publicationId

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getPublicationType(self):
        return self.publicationType

    def setPublicationType(self, publicationType):
        self.publicationType = publicationType

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price

    def getQuantity(self):
        return self.quantity

    def setQuantity(self, quantity):
        self.quantity = quantity

    def getFrequency(self):
        return self.frequency

    def setFrequency(self, frequency):
        self.frequency = frequency

    def getActive(self):
        return self.active

    def setActive(self, active):
        self.active = active

    def verifyLowStock(self):
        return self.quantity <= 5

    def verify_text(self, value):
        return isinstance(value, str) and value.strip() != ""

    def verify_price(self, price):
        return type(price) in (int, float) and price >= 0

    def verify_quantity(self, quantity):
        return type(quantity) is int and quantity >= 0

    def create_publication(self, publicationId, name, publicationType,
                           price, quantity, frequency):
        if type(publicationId) is not int or publicationId <= 0:
            return False
        if not all(self.verify_text(x) for x in (name, publicationType, frequency)):
            return False
        if not self.verify_price(price) or not self.verify_quantity(quantity):
            return False

        self.publicationId = publicationId
        self.name = name
        self.publicationType = publicationType
        self.price = price
        self.quantity = quantity
        self.frequency = frequency
        self.active = True
        return True