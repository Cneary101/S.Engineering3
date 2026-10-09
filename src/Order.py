class Order:
    def createOrder(self, customerId, publicationId, deliveryDays):
        raise NotImplementedError

    def getCustomerId(self):
        raise NotImplementedError

    def getPublicationId(self):
        raise NotImplementedError

    def getDeliveryDays(self):
        raise NotImplementedError

    def setDeliveryDays(self, deliveryDays):
        raise NotImplementedError

    def isDueOn(self, day):
        raise NotImplementedError

    def changeOrder(self, publicationId, deliveryDays):
        raise NotImplementedError

    def cancelOrder(self):
        raise NotImplementedError
