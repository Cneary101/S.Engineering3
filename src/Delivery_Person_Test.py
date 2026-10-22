import unittest
import DeliveryPerson

class DeliveryPersonTest(unittest.TestCase):

    #We test with a valid name without spaces
    def testValidName(self):
        d = DeliveryPerson.Delivery_Person(1, "Jakub")
        self.assertTrue(d.verifyName())
    #We test witha valid name WITH spaces
    def testValidNameSpaces(self):
        d = DeliveryPerson.Delivery_Person(1, "Minnie Mouse")
        self.assertTrue(d.verifyName())
    #We test with an invalid name that contains only spaces
    def testAllSpaces(self):
        d = DeliveryPerson.Delivery_Person(1, "   ")
        self.assertFalse(d.verifyName())
    #We test an invalid name that contains numbers
    def testInvalidNameNumber(self):
        d = DeliveryPerson.Delivery_Person(1, "Jakub123")
        self.assertFalse(d.verifyName())

if __name__ == '__main__':
    unittest.main()
