import unittest
from Order import Order


class OrderTest(unittest.TestCase):
    # TC01 - US09: Create an order for customer 1 and publication 3.
    def testCreateOrder(self):
        order = Order()
        order.createOrder(1, 3, ["Monday"])
        self.assertEqual(order.getCustomerId(), 1)
        self.assertEqual(order.getPublicationId(), 3)

    # TC02 - US10: Deliver on Tuesday, not Monday.
    def testSetDeliveryDays(self):
        order = Order()
        order.createOrder(1, 3, ["Monday"])
        order.setDeliveryDays(["Tuesday"])
        self.assertTrue(order.isDueOn("Tuesday"))
        self.assertFalse(order.isDueOn("Monday"))

    # TC03 - US11: Keep separate days for two publications.
    def testDifferentPublicationsOnDifferentDays(self):
        firstOrder = Order()
        firstOrder.createOrder(1, 3, ["Monday"])
        secondOrder = Order()
        secondOrder.createOrder(1, 4, ["Saturday"])
        self.assertEqual(firstOrder.getDeliveryDays(), ["Monday"])
        self.assertEqual(secondOrder.getDeliveryDays(), ["Saturday"])

    # TC04 - US12: Change the publication to 4.
    def testChangeOrder(self):
        order = Order()
        order.createOrder(1, 3, ["Monday"])
        order.changeOrder(4, ["Friday"])
        self.assertEqual(order.getPublicationId(), 4)

    # TC05 - US13: A cancelled order is not due.
    def testCancelOrder(self):
        order = Order()
        order.createOrder(1, 3, ["Monday"])
        order.cancelOrder()
        self.assertFalse(order.isDueOn("Monday"))


if __name__ == "__main__":
    unittest.main()
