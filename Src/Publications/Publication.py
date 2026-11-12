from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import engine
from models import Publication


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------
def verify_text(value):
    return isinstance(value, str) and value.strip() != ""


def verify_price(price):
    # Accept int or float, must be >= 0
    return type(price) in (int, float) and price >= 0


def verify_quantity(quantity):
    # Must be a whole number >= 0
    return type(quantity) is int and quantity >= 0


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def create_publication(publication_id, name, publication_type, price, quantity):
    # ---- validation ----
    if not isinstance(publication_id, int) or publication_id <= 0:
        return False
    if not verify_text(name) or not verify_text(publication_type):
        return False
    if not verify_price(price) or not verify_quantity(quantity):
        return False

    # ---- persist ----
    with Session(engine) as session:
        if session.get(Publication, publication_id) is not None:
            return False  # duplicate ID

        publication = Publication(
            id=publication_id,
            name=name.strip(),
            publication_type=publication_type.strip(),
            price=price,
            quantity=quantity,
        )
        session.add(publication)
        session.commit()
        return publication_id


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
def read_publication(publication_id):
    with Session(engine) as session:
        return session.get(Publication, publication_id)


def read_all_publications():
    with Session(engine) as session:
        return list(session.scalars(select(Publication).order_by(Publication.id)))


def verify_low_stock(publication):
    """Five or fewer is considered low stock. Preserved from teammate's class."""
    return publication is not None and publication.quantity <= 5


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def update_publication(publication_id, name, publication_type, price, quantity):
    # ---- validation ----
    if not verify_text(name) or not verify_text(publication_type):
        return False
    if not verify_price(price) or not verify_quantity(quantity):
        return False

    with Session(engine) as session:
        publication = session.get(Publication, publication_id)
        if publication is None:
            return False

        publication.name = name.strip()
        publication.publication_type = publication_type.strip()
        publication.price = price
        publication.quantity = quantity
        session.commit()
        return True


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def delete_publication(publication_id):
    with Session(engine) as session:
        publication = session.get(Publication, publication_id)
        if publication is None:
            return False
        try:
            session.delete(publication)
            session.commit()
            return True
        except IntegrityError:
            # publication is referenced by OrderItem → cannot delete
            session.rollback()
            return False