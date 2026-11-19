"""Tests for the customer functions.

Every test runs against a new, empty in-memory database, so nothing is
written to newsagent.db.
"""
from datetime import date

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

# customer.py lives in the Customer folder, so import it under the name "customer".
from Customer import Customer as customer
from database import Base
from models import Order

VALID = (1, "Adam", "Canavan", "0871234567", "Athlone")
OTHER = (2, "Jon", "Jones", "0869876543", "Roscommon")


@pytest.fixture(autouse=True)
def test_engine(monkeypatch):
    engine = create_engine("sqlite:///:memory:")

    # Same foreign key setting as database.py, so deletes are checked here too.
    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    # The customer functions use this engine instead of the real database.
    monkeypatch.setattr(customer, "engine", engine)
    yield engine
    engine.dispose()


def add_order(engine, customer_id):
    """Give a customer an order, so the database refuses to delete them."""
    with Session(engine) as session:
        session.add(Order(customer_id=customer_id, delivery_date=date(2026, 11, 1),
                          status="Delivered", total_amount=3))
        session.commit()


def fields(c):
    return (c.name, c.last_name, c.phone, c.address)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("good", ["Adam", "A", "  Adam  ", "Seán", "O'Brien",
                                  "Mary-Kate", "Mary Ann"])
def test_verify_name_valid(good):
    assert customer.verify_name(good) is True


@pytest.mark.parametrize("bad", ["", "   ", "Adam123", "Adam!", None, 123])
def test_verify_name_invalid(bad):
    assert customer.verify_name(bad) is False


def test_verify_id_valid():
    assert customer.verify_id(1) is True


@pytest.mark.parametrize("bad", [0, -1, "1", 1.0, None, True])
def test_verify_id_invalid(bad):
    assert customer.verify_id(bad) is False


@pytest.mark.parametrize("good", ["Athlone", "12 Main St.", None])
def test_verify_address_valid(good):
    assert customer.verify_address(good) is True


@pytest.mark.parametrize("bad", [5, ["Athlone"]])
def test_verify_address_invalid(bad):
    assert customer.verify_address(bad) is False


def test_verify_phone_number_valid():
    assert customer.verify_phone_number("0871234567") is True


@pytest.mark.parametrize("bad", ["", "087123456", "08712345678", "08712345ab",
                                 "087 123 4567", "+353871234567", None, 871234567])
def test_verify_phone_number_invalid(bad):
    assert customer.verify_phone_number(bad) is False


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def test_create_returns_id():
    assert customer.create_customer(*VALID) == 1


def test_create_stores_every_field():
    customer.create_customer(*VALID)
    assert fields(customer.read_customer(1)) == ("Adam", "Canavan", "0871234567", "Athlone")


def test_create_strips_spaces():
    customer.create_customer(1, "  Adam ", " Canavan  ", "0871234567", "  Athlone ")
    assert fields(customer.read_customer(1)) == ("Adam", "Canavan", "0871234567", "Athlone")


@pytest.mark.parametrize("address", [None, ""])
def test_create_without_address(address):
    assert customer.create_customer(1, "Adam", "Canavan", "0871234567", address) == 1
    assert customer.read_customer(1).address is None


def test_create_non_string_address_returns_false():
    assert customer.create_customer(1, "Adam", "Canavan", "0871234567", 5) is False
    assert customer.read_all_customers() == []


def test_create_duplicate_id_returns_false():
    customer.create_customer(*VALID)
    assert customer.create_customer(1, "Jon", "Jones", "0869876543", "Roscommon") is False


def test_create_duplicate_id_keeps_original():
    customer.create_customer(*VALID)
    customer.create_customer(1, "Jon", "Jones", "0869876543", "Roscommon")
    assert customer.read_customer(1).name == "Adam"


@pytest.mark.parametrize("bad_id", [0, -1, "1", 1.0, None, True])
def test_create_invalid_id_returns_false(bad_id):
    assert customer.create_customer(bad_id, "Adam", "Canavan", "0871234567", "Athlone") is False
    assert customer.read_all_customers() == []


@pytest.mark.parametrize("bad", [
    (1, "", "Canavan", "0871234567", "Athlone"),
    (1, "Adam", "", "0871234567", "Athlone"),
    (1, "   ", "Canavan", "0871234567", "Athlone"),
    (1, "Adam123", "Canavan", "0871234567", "Athlone"),
    (1, "Adam", "Canavan", "087123456", "Athlone"),
    (1, "Adam", "Canavan", None, "Athlone"),
])
def test_create_invalid_field_saves_nothing(bad):
    assert customer.create_customer(*bad) is False
    assert customer.read_all_customers() == []


def test_create_two_customers_keeps_both():
    customer.create_customer(*VALID)
    customer.create_customer(*OTHER)
    assert customer.read_customer(1).name == "Adam"
    assert customer.read_customer(2).name == "Jon"


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
def test_read_existing_customer():
    customer.create_customer(*VALID)
    assert customer.read_customer(1).last_name == "Canavan"


def test_read_missing_customer_returns_none():
    assert customer.read_customer(999) is None


@pytest.mark.parametrize("bad_id", [0, "1", True])
def test_read_invalid_id_returns_none(bad_id):
    customer.create_customer(*VALID)
    assert customer.read_customer(bad_id) is None


def test_read_all_empty():
    assert customer.read_all_customers() == []


def test_read_all_returns_every_customer_in_id_order():
    customer.create_customer(*OTHER)
    customer.create_customer(*VALID)
    assert [c.id for c in customer.read_all_customers()] == [1, 2]


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def test_update_returns_true():
    customer.create_customer(*VALID)
    assert customer.update_customer(1, "Jon", "Jones", "0869876543", "Roscommon") is True


def test_update_changes_every_field():
    customer.create_customer(*VALID)
    customer.update_customer(1, "Jon", "Jones", "0869876543", "Roscommon")
    assert fields(customer.read_customer(1)) == ("Jon", "Jones", "0869876543", "Roscommon")


def test_update_strips_spaces():
    customer.create_customer(*VALID)
    customer.update_customer(1, " Jon ", " Jones ", "0869876543", " Roscommon ")
    assert fields(customer.read_customer(1)) == ("Jon", "Jones", "0869876543", "Roscommon")


def test_update_can_remove_address():
    customer.create_customer(*VALID)
    customer.update_customer(1, "Adam", "Canavan", "0871234567", None)
    assert customer.read_customer(1).address is None


def test_update_missing_customer_returns_false():
    assert customer.update_customer(999, "Adam", "Canavan", "0871234567", "Athlone") is False


@pytest.mark.parametrize("bad_id", [0, "1", True])
def test_update_invalid_id_changes_nothing(bad_id):
    customer.create_customer(*VALID)
    assert customer.update_customer(bad_id, "Jon", "Jones", "0869876543", "Roscommon") is False
    assert customer.read_customer(1).name == "Adam"


def test_update_missing_customer_creates_nothing():
    customer.update_customer(999, "Adam", "Canavan", "0871234567", "Athlone")
    assert customer.read_all_customers() == []


@pytest.mark.parametrize("bad", [
    ("", "Jones", "0869876543", "Roscommon"),
    ("Jon", "", "0869876543", "Roscommon"),
    ("Jon123", "Jones", "0869876543", "Roscommon"),
    ("Jon", "Jones", "bad", "Roscommon"),
    ("Jon", "Jones", "0869876543", 5),
])
def test_update_invalid_field_changes_nothing(bad):
    customer.create_customer(*VALID)
    assert customer.update_customer(1, *bad) is False
    assert fields(customer.read_customer(1)) == ("Adam", "Canavan", "0871234567", "Athlone")


def test_update_leaves_other_customers_unchanged():
    customer.create_customer(*VALID)
    customer.create_customer(*OTHER)
    customer.update_customer(1, "New", "Name", "0851112222", "New Road")
    assert customer.read_customer(2).name == "Jon"


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def test_delete_returns_true():
    customer.create_customer(*VALID)
    assert customer.delete_customer(1) is True


def test_delete_removes_customer():
    customer.create_customer(*VALID)
    customer.delete_customer(1)
    assert customer.read_customer(1) is None


def test_delete_missing_customer_returns_false():
    assert customer.delete_customer(999) is False


def test_delete_twice_returns_false():
    customer.create_customer(*VALID)
    customer.delete_customer(1)
    assert customer.delete_customer(1) is False


@pytest.mark.parametrize("bad_id", [0, "1", True])
def test_delete_invalid_id_returns_false(bad_id):
    customer.create_customer(*VALID)
    assert customer.delete_customer(bad_id) is False
    assert customer.read_customer(1) is not None


def test_delete_leaves_other_customers():
    customer.create_customer(*VALID)
    customer.create_customer(*OTHER)
    customer.delete_customer(1)
    assert customer.read_customer(2) is not None


def test_delete_customer_with_order_is_refused(test_engine):
    customer.create_customer(*VALID)
    add_order(test_engine, 1)
    assert customer.delete_customer(1) is False


def test_delete_customer_with_order_keeps_customer(test_engine):
    customer.create_customer(*VALID)
    add_order(test_engine, 1)
    customer.delete_customer(1)
    assert customer.read_customer(1) is not None