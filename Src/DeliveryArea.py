from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine
from models import DeliveryArea


def read_area(area_id):
    """Return a DeliveryArea row or None."""
    with Session(engine) as session:
        return session.get(DeliveryArea, area_id)


def read_all_areas():
    """Return all areas sorted by name."""
    with Session(engine) as session:
        return list(
            session.scalars(select(DeliveryArea).order_by(DeliveryArea.name))
        )