"""Tests for the delivery person functions.

Every test runs against a new in-memory database containing two delivery
areas, so nothing is written to newsagent.db.
"""
from datetime import date

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

import DeliveryPerson as dp
from database import Base
from models import DeliveryArea, Route

VALID = (1, "Jakub", 1)
OTHER = (2, "Mary O'Brien", 2)


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
    with Session(engine) as session:
        session.add_all([DeliveryArea(id=1, name="Athlone"), DeliveryArea(id=2, name="Moate")])
        session.commit()

    # The delivery person functions use this engine instead of the real database.
    monkeypatch.setattr(dp, "engine", engine)
    yield engine
    engine.dispose()


def add_route(engine, driver_id):
    """Give a driver a route, so the database refuses to delete them."""
    with Session(engine) as session:
        session.add(Route(date=date(2026, 11, 1), driver_id=driver_id, status="Planned"))
        session.commit()


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("good", ["Jakub", "Minnie Mouse", "Mary O'Brien", "Mary-Kate",
                                  "Seán", "  Jakub  "])
def test_verify_name_valid(good):
    assert dp.verify_name(good) is True


@pytest.mark.parametrize("bad", ["", "   ", "Jakub123", "Jakub!", "J@kub", None, 123])
def test_verify_name_invalid(bad):
    assert dp.verify_name(bad) is False


def test_verify_id_valid():
    assert dp.verify_id(1) is True


@pytest.mark.parametrize("bad", [0, -1, "1", 1.0, None, True])
def test_verify_id_invalid(bad):
    assert dp.verify_id(bad) is False


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def test_create_returns_id():
    assert dp.create_delivery_person(*VALID) == 1


def test_create_stores_every_field():
    dp.create_delivery_person(*VALID)
    person = dp.read_delivery_person(1)
    assert (person.name, person.area_id) == ("Jakub", 1)


def test_create_strips_name():
    dp.create_delivery_person(1, "  Jakub  ", 1)
    assert dp.read_delivery_person(1).name == "Jakub"


def test_create_duplicate_id_returns_false():
    dp.create_delivery_person(*VALID)
    assert dp.create_delivery_person(1, "Tom", 2) is False


def test_create_duplicate_id_keeps_original():
    dp.create_delivery_person(*VALID)
    dp.create_delivery_person(1, "Tom", 2)
    assert dp.read_delivery_person(1).name == "Jakub"


@pytest.mark.parametrize("bad_id", [0, -1, "1", None, True])
def test_create_invalid_id_saves_nothing(bad_id):
    assert dp.create_delivery_person(bad_id, "Jakub", 1) is False
    assert dp.read_all_delivery_persons() == []


@pytest.mark.parametrize("bad_area", [0, -1, "1", None, True])
def test_create_invalid_area_id_saves_nothing(bad_area):
    assert dp.create_delivery_person(1, "Jakub", bad_area) is False
    assert dp.read_all_delivery_persons() == []


def test_create_missing_area_saves_nothing():
    assert dp.create_delivery_person(1, "Jakub", 99) is False
    assert dp.read_all_delivery_persons() == []


@pytest.mark.parametrize("bad_name", ["", "Jakub123", None])
def test_create_invalid_name_saves_nothing(bad_name):
    assert dp.create_delivery_person(1, bad_name, 1) is False
    assert dp.read_all_delivery_persons() == []


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
def test_read_existing_driver():
    dp.create_delivery_person(*VALID)
    assert dp.read_delivery_person(1).name == "Jakub"


def test_read_missing_driver_returns_none():
    assert dp.read_delivery_person(999) is None


@pytest.mark.parametrize("bad_id", [0, "1", True])
def test_read_invalid_id_returns_none(bad_id):
    dp.create_delivery_person(*VALID)
    assert dp.read_delivery_person(bad_id) is None


def test_read_all_empty():
    assert dp.read_all_delivery_persons() == []


def test_read_all_returns_every_driver_in_id_order():
    dp.create_delivery_person(*OTHER)
    dp.create_delivery_person(*VALID)
    assert [p.id for p in dp.read_all_delivery_persons()] == [1, 2]


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def test_update_returns_true():
    dp.create_delivery_person(*VALID)
    assert dp.update_delivery_person(1, "Jakub Nowak", 1) is True


def test_update_changes_name():
    dp.create_delivery_person(*VALID)
    dp.update_delivery_person(1, " Jakub Nowak ", 1)
    assert dp.read_delivery_person(1).name == "Jakub Nowak"


def test_update_moves_driver_to_another_area():
    dp.create_delivery_person(*VALID)
    dp.update_delivery_person(1, "Jakub", 2)
    assert dp.read_delivery_person(1).area_id == 2


def test_update_missing_driver_returns_false():
    assert dp.update_delivery_person(999, "Jakub", 1) is False


def test_update_missing_driver_creates_nothing():
    dp.update_delivery_person(999, "Jakub", 1)
    assert dp.read_all_delivery_persons() == []


@pytest.mark.parametrize("bad", [
    ("", 2),
    ("Jakub123", 2),
    ("Tom", 99),
    ("Tom", True),
])
def test_update_invalid_details_change_nothing(bad):
    dp.create_delivery_person(*VALID)
    assert dp.update_delivery_person(1, *bad) is False
    person = dp.read_delivery_person(1)
    assert (person.name, person.area_id) == ("Jakub", 1)


def test_update_leaves_other_drivers_unchanged():
    dp.create_delivery_person(*VALID)
    dp.create_delivery_person(*OTHER)
    dp.update_delivery_person(1, "Tom", 2)
    assert dp.read_delivery_person(2).name == "Mary O'Brien"


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def test_delete_returns_true():
    dp.create_delivery_person(*VALID)
    assert dp.delete_delivery_person(1) is True


def test_delete_removes_driver():
    dp.create_delivery_person(*VALID)
    dp.delete_delivery_person(1)
    assert dp.read_delivery_person(1) is None


def test_delete_missing_driver_returns_false():
    assert dp.delete_delivery_person(999) is False


def test_delete_twice_returns_false():
    dp.create_delivery_person(*VALID)
    dp.delete_delivery_person(1)
    assert dp.delete_delivery_person(1) is False


@pytest.mark.parametrize("bad_id", [0, "1", True])
def test_delete_invalid_id_returns_false(bad_id):
    dp.create_delivery_person(*VALID)
    assert dp.delete_delivery_person(bad_id) is False
    assert dp.read_delivery_person(1) is not None


def test_delete_leaves_other_drivers():
    dp.create_delivery_person(*VALID)
    dp.create_delivery_person(*OTHER)
    dp.delete_delivery_person(1)
    assert dp.read_delivery_person(2) is not None


def test_delete_driver_with_route_is_refused(test_engine):
    dp.create_delivery_person(*VALID)
    add_route(test_engine, 1)
    assert dp.delete_delivery_person(1) is False


def test_delete_driver_with_route_keeps_driver(test_engine):
    dp.create_delivery_person(*VALID)
    add_route(test_engine, 1)
    dp.delete_delivery_person(1)
    assert dp.read_delivery_person(1) is not None