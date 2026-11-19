from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import engine
from models import DeliveryPerson, DeliveryArea


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------
def verify_id(value):
    # type() rather than isinstance(), so True and False are rejected
    return type(value) is int and value > 0


def verify_name(name):
    # Letters, spaces, apostrophes and hyphens only, e.g. "Mary O'Brien", "Mary-Kate".
    # isalpha() also accepts accented letters such as "Seán".
    if not isinstance(name, str) or name.strip() == "":
        return False
    return all(char.isalpha() or char in " '-" for char in name.strip())


def _area_exists(session, area_id):
    return session.get(DeliveryArea, area_id) is not None


def _save(session):
    # Commit changes, or undo them if the database rejects them.
    try:
        session.commit()
        return True
    except SQLAlchemyError:
        session.rollback()
        return False


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def create_delivery_person(person_id, name, area_id):
    if not verify_id(person_id) or not verify_name(name) or not verify_id(area_id):
        return False

    with Session(engine) as session:
        if session.get(DeliveryPerson, person_id) is not None:
            return False  # duplicate ID
        if not _area_exists(session, area_id):
            return False  # area must exist

        session.add(DeliveryPerson(id=person_id, name=name.strip(), area_id=area_id))
        if not _save(session):
            return False
        return person_id


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
def read_delivery_person(person_id):
    if not verify_id(person_id):
        return None
    with Session(engine) as session:
        return session.get(DeliveryPerson, person_id)


def read_all_delivery_persons():
    with Session(engine) as session:
        return list(session.scalars(select(DeliveryPerson).order_by(DeliveryPerson.id)))


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def update_delivery_person(person_id, name, area_id):
    if not verify_id(person_id) or not verify_name(name) or not verify_id(area_id):
        return False

    with Session(engine) as session:
        person = session.get(DeliveryPerson, person_id)
        if person is None:
            return False
        if not _area_exists(session, area_id):
            return False

        person.name = name.strip()
        person.area_id = area_id
        return _save(session)


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def delete_delivery_person(person_id):
    # Returns False if the driver doesn't exist, or if they have routes
    # (the database refuses to delete them). Call read_delivery_person first
    # to tell the two apart.
    if not verify_id(person_id):
        return False

    with Session(engine) as session:
        person = session.get(DeliveryPerson, person_id)
        if person is None:
            return False
        session.delete(person)
        return _save(session)