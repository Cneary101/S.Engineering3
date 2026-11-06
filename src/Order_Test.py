import pytest
from src.Order import OrderManager
from src.Customer.Customer import CustomerManager
from src.Publications.Publications import Publication

VALID = (1, 1, ["Monday"])
OTHER = (1, 2, ["Friday"])


@pytest.fixture
def manager():
    customers = CustomerManager()
    customers.create_customer(
        "Alina", "Stavratii", "Athlone", "0899679339"
    )

    publications = {
        1: Publication(1, "Irish Times", "Newspaper", 3, 10, "Daily"),
        2: Publication(2, "Independent", "Newspaper", 3, 10, "Daily")
    }

    return OrderManager(customers, publications)


# Create
def test_create_order(manager):
    order_id = manager.create_order(*VALID)
    order = manager.read_order(order_id)

    assert order_id == 1
    assert order.customer_id == 1
    assert order.publication_id == 1
    assert order.delivery_days == ["Monday"]


def test_unique_ids(manager):
    first_id = manager.create_order(*VALID)
    second_id = manager.create_order(*OTHER)

    assert first_id != second_id
    assert len(manager.read_all_orders()) == 2


def test_unknown_customer(manager):
    assert manager.create_order(99, 1, ["Monday"]) is False
    assert manager.read_all_orders() == {}


def test_unknown_publication(manager):
    assert manager.create_order(1, 99, ["Monday"]) is False
    assert manager.read_all_orders() == {}


def test_empty_days(manager):
    assert manager.create_order(1, 1, []) is False
    assert manager.read_all_orders() == {}


# Read
def test_read_order(manager):
    order_id = manager.create_order(*VALID)

    assert manager.read_order(order_id).publication_id == 1


# Update
def test_update_order(manager):
    order_id = manager.create_order(*VALID)

    assert manager.update_order(order_id, 2, ["Friday"]) is True

    order = manager.read_order(order_id)
    assert order.publication_id == 2
    assert order.delivery_days == ["Friday"]


def test_invalid_update(manager):
    order_id = manager.create_order(*VALID)

    assert manager.update_order(order_id, 2, ["Funday"]) is False

    order = manager.read_order(order_id)
    assert order.publication_id == 1
    assert order.delivery_days == ["Monday"]


# Delete (cancel)
def test_cancel_order(manager):
    order_id = manager.create_order(*VALID)

    assert manager.delete_order(order_id) is True
    assert manager.read_order(order_id).active is False
