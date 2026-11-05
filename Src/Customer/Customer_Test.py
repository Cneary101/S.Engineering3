import pytest
from Customer.Customer import Customer, CustomerManager

VALID = ("Adam", "Canavan", "Athlone", "0871234567")
OTHER = ("Jon", "jones", "Roscommon", "0869876543")


@pytest.fixture
def manager():
    return CustomerManager()


# Validation
@pytest.mark.parametrize("good", ["Adam", "A"])
def test_valid_first_name(good):
    assert Customer.verify_first_name(good) is True


@pytest.mark.parametrize("bad", ["", None, 123])
def test_invalid_first_name(bad):
    assert Customer.verify_first_name(bad) is False


@pytest.mark.parametrize("good", ["Canavan", "C"])
def test_valid_last_name(good):
    assert Customer.verify_last_name(good) is True


@pytest.mark.parametrize("bad", ["", None, 123])
def test_invalid_last_name(bad):
    assert Customer.verify_last_name(bad) is False


def test_valid_address():
    assert Customer.verify_address("Athlone") is True


@pytest.mark.parametrize("bad", ["", None, 123])
def test_invalid_address(bad):
    assert Customer.verify_address(bad) is False


def test_valid_phone_number():
    assert Customer.verify_phone_number("0871234567") is True


@pytest.mark.parametrize(
    "bad",
    ["", "087123456", "08712345678", "0871234567abc", "9999999999999", None],
)
def test_invalid_phone_number(bad):
    assert Customer.verify_phone_number(bad) is False


# Create
def test_create_stores_customer(manager):
    customer_id = manager.create_customer(*VALID)
    customer = manager.read_customer(customer_id)
    assert customer.first_name == "Adam"
    assert customer.last_name == "Canavan"
    assert customer.address == "Athlone"
    assert customer.phone_number == "0871234567"


def test_create_invalid_returns_false_and_stores_nothing(manager):
    assert manager.create_customer("Adam", "Canavan", "Athlone", "bad") is False
    assert manager.read_all_customers() == {}


def test_create_two_customers_keeps_both(manager):
    first_id = manager.create_customer(*VALID)
    second_id = manager.create_customer(*OTHER)
    assert first_id != second_id
    assert manager.read_customer(first_id).first_name == "Adam"
    assert manager.read_customer(second_id).first_name == "Ann"


# Read
def test_read_missing_customer_returns_none(manager):
    assert manager.read_customer(999) is None


def test_read_all_empty(manager):
    assert manager.read_all_customers() == {}


def test_read_all_returns_every_customer(manager):
    manager.create_customer(*VALID)
    manager.create_customer(*OTHER)
    assert len(manager.read_all_customers()) == 2


def test_read_all_returns_a_copy(manager):
    customer_id = manager.create_customer(*VALID)
    manager.read_all_customers().clear()
    assert manager.read_customer(customer_id) is not None


# Update
def test_update_changes_all_fields_and_keeps_id(manager):
    customer_id = manager.create_customer(*VALID)
    assert manager.update_customer(customer_id, *OTHER) is True
    customer = manager.read_customer(customer_id)
    assert customer.first_name == "Ann"
    assert customer.last_name == "Byrne"
    assert customer.address == "1 Main St"
    assert customer.phone_number == "0869876543"


def test_update_missing_customer_adds_nothing(manager):
    assert manager.update_customer(999, *VALID) is False
    assert manager.read_all_customers() == {}


def test_update_invalid_field_changes_nothing(manager):
    customer_id = manager.create_customer(*VALID)
    assert manager.update_customer(customer_id, "Ann", "Byrne", "1 Main St", "bad") is False
    customer = manager.read_customer(customer_id)
    assert customer.first_name == "Adam"
    assert customer.last_name == "Canavan"
    assert customer.address == "Athlone"
    assert customer.phone_number == "0871234567"


def test_update_leaves_other_customers_unchanged(manager):
    first_id = manager.create_customer(*VALID)
    second_id = manager.create_customer(*OTHER)
    manager.update_customer(first_id, "New", "Name", "New Road", "0851112222")
    assert manager.read_customer(second_id).first_name == "Ann"


# Delete
def test_delete_removes_customer(manager):
    customer_id = manager.create_customer(*VALID)
    assert manager.delete_customer(customer_id) is True
    assert manager.read_customer(customer_id) is None


def test_delete_missing_customer_returns_false(manager):
    assert manager.delete_customer(999) is False


def test_delete_twice_returns_false(manager):
    customer_id = manager.create_customer(*VALID)
    manager.delete_customer(customer_id)
    assert manager.delete_customer(customer_id) is False


def test_deleted_id_is_not_reused(manager):
    deleted_id = manager.create_customer(*VALID)
    manager.delete_customer(deleted_id)
    assert manager.create_customer(*OTHER) != deleted_id