import pytest
from datetime import date
from decimal import Decimal
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

import Publications.Publication as publication
from models import Base, Publication as PublicationRow, Customer, Order, OrderItem


@pytest.fixture
def database(tmp_path, monkeypatch):
    engine = create_engine(f"sqlite:///{tmp_path / 'publication_test.db'}")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, record):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    monkeypatch.setattr(publication, "engine", engine)
    yield engine
    engine.dispose()


# Validation
@pytest.mark.parametrize("value", ["Irish Times", "A", " Daily "])
def test_valid_text(value):
    assert publication.verify_text(value) is True


@pytest.mark.parametrize("value", ["", "   ", None, 123])
def test_invalid_text(value):
    assert publication.verify_text(value) is False


@pytest.mark.parametrize("value", [0, 3, 3.5])
def test_valid_price(value):
    assert publication.verify_price(value) is True


@pytest.mark.parametrize("value", [-1, -0.01, "3.5", True, None])
def test_invalid_price(value):
    assert publication.verify_price(value) is False


@pytest.mark.parametrize("value", [0, 5, 10])
def test_valid_quantity(value):
    assert publication.verify_quantity(value) is True


@pytest.mark.parametrize("value", [-1, 2.5, "5", True, None])
def test_invalid_quantity(value):
    assert publication.verify_quantity(value) is False


# Create and Read
@pytest.mark.parametrize("publication_id,name,ptype,price,quantity", [
    (0, "Irish Times", "Newspaper", 3.5, 10),
    (-1, "Irish Times", "Newspaper", 3.5, 10),
    (True, "Irish Times", "Newspaper", 3.5, 10),
    ("1", "Irish Times", "Newspaper", 3.5, 10),
    (1, "", "Newspaper", 3.5, 10),
    (1, "Irish Times", "   ", 3.5, 10),
    (1, "Irish Times", "Newspaper", -1, 10),
    (1, "Irish Times", "Newspaper", 3.5, -1),
    (1, "Irish Times", "Newspaper", 3.5, 2.5),
])
def test_invalid_creation(database, publication_id, name, ptype, price, quantity):
    assert publication.create_publication(publication_id, name, ptype, price, quantity) is False
    assert publication.read_all_publications() == []


def test_create_read_and_list(database):
    assert publication.create_publication(1, "  Irish Times ", " Newspaper ", 3.5, 10) == 1
    assert publication.create_publication(2, "Independent", "Newspaper", 2, 6) == 2
    row = publication.read_publication(1)
    assert row.name == "Irish Times"
    assert row.publication_type == "Newspaper"
    assert row.price == Decimal("3.5")
    assert row.quantity == 10
    assert [item.id for item in publication.read_all_publications()] == [1, 2]
    assert publication.read_publication(99) is None


def test_duplicate_id_keeps_original(database):
    publication.create_publication(1, "Irish Times", "Newspaper", 3.5, 10)
    assert publication.create_publication(1, "Other", "Magazine", 4, 5) is False
    assert publication.read_publication(1).name == "Irish Times"
    assert len(publication.read_all_publications()) == 1


# Update
@pytest.mark.parametrize("name,ptype,price,quantity", [
    ("", "Newspaper", 3, 5),
    ("Irish Times", " ", 3, 5),
    ("Irish Times", "Newspaper", -1, 5),
    ("Irish Times", "Newspaper", 3, 1.5),
])
def test_invalid_update_keeps_existing_values(database, name, ptype, price, quantity):
    publication.create_publication(1, "Original", "Newspaper", 2, 10)
    assert publication.update_publication(1, name, ptype, price, quantity) is False
    row = publication.read_publication(1)
    assert (row.name, row.publication_type, row.price, row.quantity) == ("Original", "Newspaper", 2, 10)


def test_update_and_missing_id(database):
    publication.create_publication(1, "Original", "Newspaper", 2, 10)
    assert publication.update_publication(1, "  Updated  ", " Magazine ", 4.5, 5) is True
    row = publication.read_publication(1)
    assert (row.name, row.publication_type, row.price, row.quantity) == ("Updated", "Magazine", Decimal("4.5"), 5)
    assert publication.update_publication(99, "Other", "Magazine", 2, 5) is False


# Low stock and Delete
@pytest.mark.parametrize("quantity,expected", [(0, True), (5, True), (6, False)])
def test_low_stock(database, quantity, expected):
    publication.create_publication(1, "Irish Times", "Newspaper", 3, quantity)
    assert publication.verify_low_stock(publication.read_publication(1)) is expected
    assert publication.verify_low_stock(None) is False


def test_delete_and_missing_record(database):
    assert publication.delete_publication(99) is False
    publication.create_publication(1, "Irish Times", "Newspaper", 3, 10)
    assert publication.delete_publication(1) is True
    assert publication.read_publication(1) is None
    assert publication.read_all_publications() == []


def test_delete_blocked_when_order_item_references_publication(database):
    publication.create_publication(1, "Irish Times", "Newspaper", 3, 10)
    with Session(database) as session:
        session.add(Customer(id=1, name="John", last_name="Smith", phone="0871234567"))
        session.add(Order(id=1, customer_id=1, delivery_date=date(2026, 11, 19), status="pending", total_amount=3))
        session.add(OrderItem(id=1, order_id=1, publication_id=1, quantity=1))
        session.commit()
    assert publication.delete_publication(1) is False
    assert publication.read_publication(1) is not None


def test_record_is_saved_in_sql(database):
    publication.create_publication(1, "Irish Times", "Newspaper", 3, 10)
    with Session(database) as session:
        assert session.get(PublicationRow, 1).name == "Irish Times"
