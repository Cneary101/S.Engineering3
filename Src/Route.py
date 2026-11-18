from datetime import date as date_type

from sqlalchemy import select
from sqlalchemy.orm import Session

from constants import ROUTE_STATUSES
from database import engine
from models import Route, DeliveryPerson


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------
def _driver_exists(session, driver_id):
    return session.get(DeliveryPerson, driver_id) is not None


def _valid_date(value):
    """Accept a datetime.date. Callers convert user input first."""
    return isinstance(value, date_type)


def _valid_status(value):
    return isinstance(value, str) and value in ROUTE_STATUSES


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def create_route(route_id, route_date, driver_id, status):
    # ---- validation ----
    if not isinstance(route_id, int) or route_id <= 0:
        return False
    if not _valid_date(route_date):
        return False
    if not isinstance(driver_id, int) or driver_id <= 0:
        return False
    if not _valid_status(status):
        return False

    with Session(engine) as session:
        if session.get(Route, route_id) is not None:
            return False  # duplicate ID
        if not _driver_exists(session, driver_id):
            return False  # FK target missing

        route = Route(
            id=route_id,
            date=route_date,
            driver_id=driver_id,
            status=status,
        )
        session.add(route)
        session.commit()
        return route_id


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
def read_route(route_id):
    with Session(engine) as session:
        return session.get(Route, route_id)


def read_all_routes():
    with Session(engine) as session:
        return list(session.scalars(select(Route).order_by(Route.date, Route.id)))


def read_routes_by_driver(driver_id):
    """Return all routes assigned to a specific driver. Useful for reports."""
    with Session(engine) as session:
        return list(
            session.scalars(
                select(Route)
                .where(Route.driver_id == driver_id)
                .order_by(Route.date)
            )
        )


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def update_route(route_id, route_date, driver_id, status):
    # ---- validation ----
    if not _valid_date(route_date):
        return False
    if not isinstance(driver_id, int) or driver_id <= 0:
        return False
    if not _valid_status(status):
        return False

    with Session(engine) as session:
        route = session.get(Route, route_id)
        if route is None:
            return False
        if not _driver_exists(session, driver_id):
            return False

        route.date = route_date
        route.driver_id = driver_id
        route.status = status
        session.commit()
        return True


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def delete_route(route_id):
    with Session(engine) as session:
        route = session.get(Route, route_id)
        if route is None:
            return False
        session.delete(route)
        session.commit()
        return True