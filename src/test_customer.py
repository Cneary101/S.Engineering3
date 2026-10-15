import pytest
from Create_Customer import Create_Customer

@pytest.fixture
def c1():
    return Create_Customer()

def test_valid_first_name(c1):
    assert c1.verify_first_name("Adam") is True

def test_invalid_firstname(c1):
    assert c1.verify_first_name("") is False

def test_invalid_last_name(c1):
    assert c1.verify_last_name("") is False

def test_invalid_phone_number(c1):
    assert c1.verify_phone_number("9999999999999") is False

def test_valid_phone_number(c1):
    assert c1.verify_phone_number("0871234567") is True

@pytest.mark.parametrize("bad",["","087123456","08712345678","0871234567abc", None ] )
def test_invalid_phone_number(c1,bad):
    assert c1.verify_phone_number(bad) is False

def test_valid_account_created(c1):
    assert c1.create_customer("Adam", "Canavan","Retreat Road","0871234567") is True
    assert c1.first_name == "Adam" and c1.last_name == "Canavan"
