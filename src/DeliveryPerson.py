from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import engine
from models import DeliveryPerson, DeliveryArea


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------
def verify_text(value):
    return isinstance(value, str) and value.strip() != ""


def _area_exists(session, area_id):
    return session.get(DeliveryArea, area_id) is not None


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def create_delivery_person(person_id, name, area_id):
    # ---- validation ----
    if not isinstance(person_id, int) or person_id <= 0:
        return False
    if not verify_text(name):
        return False
    if not isinstance(area_id, int) or area_id <= 0:
        return False

    with Session(engine) as session:
        if session.get(DeliveryPerson, person_id) is not None:
            return False  # duplicate ID
        if not _area_exists(session, area_id):
            return False  # FK target missing

        person = DeliveryPerson(
            id=person_id,
            name=name.strip(),
            area_id=area_id,
        )
        session.add(person)
        session.commit()
        return person_id


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
def read_delivery_person(person_id):
    with Session(engine) as session:
        return session.get(DeliveryPerson, person_id)


def read_all_delivery_persons():
    with Session(engine) as session:
        return list(
            session.scalars(
                select(DeliveryPerson).order_by(DeliveryPerson.id)
            )
        )


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def update_delivery_person(person_id, name, area_id):
    # ---- validation ----
    if not verify_text(name):
        return False
    if not isinstance(area_id, int) or area_id <= 0:
        return False

    with Session(engine) as session:
        person = session.get(DeliveryPerson, person_id)
        if person is None:
            return False
        if not _area_exists(session, area_id):
            return False

        person.name = name.strip()
        person.area_id = area_id
        session.commit()
        return True


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def delete_delivery_person(person_id):
    with Session(engine) as session:
        person = session.get(DeliveryPerson, person_id)
        if person is None:
            return False
        try:
            session.delete(person)
            session.commit()
            return True
        except IntegrityError:
            # driver is referenced by one or more Routes
            session.rollback()
            return False