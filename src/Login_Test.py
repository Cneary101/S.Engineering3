import unittest

import Login

class MyTestCase(unittest.TestCase):
    #Username
    #
    #
    #Test a username with a valid name inside the boundaries
    def testInnerValidUsername(self):
        l=Login.Login('samuel1',' ')
        self.assertTrue(l.verifyUsername())
    #Test valid lower boundary username
    def testLowerValidUsername(self):
        l=Login.Login('samuel',' ')
        self.assertTrue(l.verifyUsername())
    #Test valid higher boundary username
    def testHigherValidUsername(self):
        l=Login.Login('samuelsamuel',' ')
        self.assertTrue(l.verifyUsername())
    #Test invalid lower out of bound username
    def testLowerInvalidUsername(self):
        l=Login.Login('samu',' ')
        self.assertFalse(l.verifyUsername())
    #Test invalid higher out of bound username
    def testHigherInvalidUsername(self):
        l=Login.Login('samuelsamuelsamuel',' ')
        self.assertFalse(l.verifyUsername())
    #Password
    #
    #Test Valid Password inside the boundaries
    def testInnerValidPassword(self):
        l=Login.Login(' ','12345')
        self.assertTrue(l.verifyPassword())
    #Test Valid Lower boundary password
    def testLowerValidPassword(self):
        l=Login.Login(' ','1234')
        self.assertTrue(l.verifyPassword())
    #Test Valid Higher boundary password
    def testHigherValidPassword(self):
        l=Login.Login(' ','123456')
        self.assertTrue(l.verifyPassword())
    #Test Invalid lower boundary password
    def testLowerInvalidPassword(self):
        l=Login.Login(' ','123')
        self.assertFalse(l.verifyPassword())
    #Test Invalid Higher Boundary password
    def testHigherInvalidPassword(self):
        l=Login.Login(' ','1234567')
        self.assertFalse(l.verifyPassword())
    #Test Invalid Non-Digits Password
    def testInnerInvalidPassword(self):
        l=Login.Login(' ','abcdf')
        self.assertFalse(l.verifyPassword())



if __name__ == '__main__':
    unittest.main()
