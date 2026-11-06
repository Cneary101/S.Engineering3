# Holds details for one publication.
class Publication:
    def __init__(self):
        # Start with an empty publication.
        self.publicationId = None
        self.name = None
        self.publicationType = None
        self.price = None
        self.quantity = None
        self.frequency = None
        self.active = None

    # Access and change individual attributes.
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

    # Check the required values before creating a publication.
    def verify_text(self, value):
        return isinstance(value, str) and value.strip() != ""

    def verify_price(self, price):
        return type(price) in (int, float) and price >= 0

    def verify_quantity(self, quantity):
        return type(quantity) is int and quantity >= 0

    # Five or fewer is considered low stock.
    def verifyLowStock(self):
        return self.quantity is not None and self.quantity <= 5

    # Only save the details when all checks pass.
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


# Handles CRUD for publications.
class PublicationManager:
    def __init__(self):
        self.publications = {}

    def create_publication(self, publicationId, name, publicationType,
                           price, quantity, frequency):
        if publicationId in self.publications:
            return False

        publication = Publication()
        if not publication.create_publication(publicationId, name, publicationType,
                                              price, quantity, frequency):
            return False

        self.publications[publicationId] = publication
        return publicationId

    def read_publication(self, publicationId):
        return self.publications.get(publicationId)

    def read_all_publications(self):
        return dict(self.publications)

    def update_publication(self, publicationId, name, publicationType,
                           price, quantity, frequency):
        publication = self.read_publication(publicationId)
        if publication is None:
            return False

        # Check every replacement value before changing anything.
        if not all(publication.verify_text(x) for x in (name, publicationType, frequency)):
            return False
        if not publication.verify_price(price) or not publication.verify_quantity(quantity):
            return False

        publication.setName(name)
        publication.setPublicationType(publicationType)
        publication.setPrice(price)
        publication.setQuantity(quantity)
        publication.setFrequency(frequency)
        return True

    def delete_publication(self, publicationId):
        # Keep the record for old orders
        publication = self.read_publication(publicationId)
        if publication is None or publication.getActive() is False:
            return False

        publication.setActive(False)
        return True
