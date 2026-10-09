class Stock:
    def createStock(self, publicationId, quantity):
        raise NotImplementedError

    def getQuantity(self):
        raise NotImplementedError

    def setQuantity(self, quantity):
        raise NotImplementedError

    def reduceQuantity(self, copies):
        raise NotImplementedError

    def getLowStockWarning(self):
        raise NotImplementedError
