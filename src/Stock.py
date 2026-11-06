class StockManager:
    def __init__(self, publications):
        self.publications = publications

    def create_stock(self, publication_id, quantity):
        if type(publication_id) is not int or publication_id <= 0:
            return False

        publication = self.publications.get(publication_id)

        if publication is None:
            return False

        if not publication.verify_quantity(quantity):
            return False

        publication.setQuantity(quantity)
        return True

    def read_stock(self, publication_id):
        if type(publication_id) is not int or publication_id <= 0:
            return None

        publication = self.publications.get(publication_id)

        if publication is None:
            return None

        quantity = publication.getQuantity()

        if not publication.verify_quantity(quantity):
            return None

        return quantity

    def update_stock(self, publication_id, quantity):
        return self.create_stock(publication_id, quantity)

    def low_stock_warning(self, publication_id):
        if self.read_stock(publication_id) is None:
            return None

        if self.publications[publication_id].verifyLowStock():
            return "Low stock"

        return ""
