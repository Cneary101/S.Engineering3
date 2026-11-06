import pytest
from src.Stock import StockManager
from src.Publications.Publications import Publication

VALID = (1, 12)
OTHER = (1, 5)


@pytest.fixture
def manager():
    publications = {
        1: Publication(1, "Irish Times", "Newspaper", 3, 10, "Daily")
    }

    return StockManager(publications)


# Create
def test_zero_quantity(manager):
    assert manager.create_stock(1, 0) is True
    assert manager.read_stock(1) == 0
    assert manager.low_stock_warning(1) == "Low stock"


def test_positive_quantity(manager):
    assert manager.create_stock(*VALID) is True
    assert manager.read_stock(1) == 12
    assert manager.low_stock_warning(1) == ""


# Validation
def test_negative_quantity(manager):
    assert manager.create_stock(1, -1) is False
    assert manager.read_stock(1) == 10


def test_decimal_quantity(manager):
    assert manager.create_stock(1, 2.5) is False
    assert manager.read_stock(1) == 10


def test_text_quantity(manager):
    assert manager.create_stock(1, "ten") is False
    assert manager.read_stock(1) == 10


def test_unknown_publication(manager):
    assert manager.create_stock(99, 10) is False
    assert manager.read_stock(99) is None


# Update and low-stock checks
def test_update_quantity(manager):
    assert manager.update_stock(*OTHER) is True
    assert manager.read_stock(1) == 5
    assert manager.low_stock_warning(1) == "Low stock"


def test_no_warning_at_six(manager):
    manager.publications[1].setQuantity(6)

    assert manager.low_stock_warning(1) == ""


def test_rejected_update(manager):
    assert manager.update_stock(1, -1) is False
    assert manager.read_stock(1) == 10
