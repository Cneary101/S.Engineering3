import unittest
from Stock import Stock


class StockTest(unittest.TestCase):
    # TC06 - US20: Update the quantity to 12.
    def testSetQuantity(self):
        stock = Stock()
        stock.createStock(3, 10)
        stock.setQuantity(12)
        self.assertEqual(stock.getQuantity(), 12)

    # TC07 - US21: Allocating 3 copies leaves 7.
    def testReduceQuantityForDocket(self):
        stock = Stock()
        stock.createStock(3, 10)
        stock.reduceQuantity(3)
        self.assertEqual(stock.getQuantity(), 7)

    # TC08 - US22: Show a warning at 5 copies.
    def testLowStockAtFive(self):
        stock = Stock()
        stock.createStock(3, 5)
        self.assertEqual(stock.getLowStockWarning(), "Low stock")


if __name__ == "__main__":
    unittest.main()
