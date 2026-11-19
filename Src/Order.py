from datetime import date as date_type

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from constants import ORDER_STATUSES
from database import engine
from models import Order, OrderItem, Customer, Publication


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------
def _valid_date(value):
    return isinstance(value, date_type)


def _valid_status(value):
    return isinstance(value, str) and value in ORDER_STATUSES


def _merge_duplicate_items(items):
    """Merge duplicate publication_ids, summing their quantities.

    Accepts: list of (publication_id, quantity) tuples.
    Returns: list of (publication_id, quantity) with duplicates merged.
    Preserves insertion order of first occurrence.
    """
    merged = {}
    for pub_id, qty in items:
        merged[pub_id] = merged.get(pub_id, 0) + qty
    return list(merged.items())


def _fetch_publication_prices(session, pub_ids):
    """Return {pub_id: price} for the requested ids. Missing ids are absent."""
    if not pub_ids:
        return {}
    rows = session.scalars(
        select(Publication).where(Publication.id.in_(pub_ids))
    ).all()
    return {p.id: float(p.price) for p in rows}


def _validate_items(session, items):
    """Validate the items list. Returns (cleaned_items, prices) or (None, None).

    cleaned_items = [(pub_id, qty), ...] with duplicates merged.
    prices        = {pub_id: price} for computing totals.
    """
    if not items:
        return None, None

    for entry in items:
        if not isinstance(entry, tuple) or len(entry) != 2:
            return None, None
        pub_id, qty = entry
        if not isinstance(pub_id, int) or pub_id <= 0:
            return None, None
        if not isinstance(qty, int) or qty <= 0:
            return None, None

    cleaned = _merge_duplicate_items(items)
    pub_ids = [pid for pid, _ in cleaned]
    prices = _fetch_publication_prices(session, pub_ids)

    # All requested publications must exist
    for pid in pub_ids:
        if pid not in prices:
            return None, None

    return cleaned, prices


def _compute_total(cleaned_items, prices):
    """Sum of quantity × price for all items."""
    return round(sum(prices[pid] * qty for pid, qty in cleaned_items), 2)


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def create_order(order_id, customer_id, delivery_date, status, items):
    """Create an order with its items in a single transaction.

    items = list of (publication_id, quantity) tuples. Must be non-empty.
    total_amount is computed; callers cannot override it.
    """
    # ---- top-level validation ----
    if not isinstance(order_id, int) or order_id <= 0:
        return False
    if not isinstance(customer_id, int) or customer_id <= 0:
        return False
    if not _valid_date(delivery_date):
        return False
    if not _valid_status(status):
        return False

    with Session(engine) as session:
        # Duplicate order ID?
        if session.get(Order, order_id) is not None:
            return False

        # Customer exists?
        if session.get(Customer, customer_id) is None:
            return False

        # Validate items (merges duplicates, checks pubs exist)
        cleaned, prices = _validate_items(session, items)
        if cleaned is None:
            return False

        total = _compute_total(cleaned, prices)

        # Insert order, then items
        order = Order(
            id=order_id,
            customer_id=customer_id,
            delivery_date=delivery_date,
            status=status,
            total_amount=total,
        )
        session.add(order)
        session.flush()  # ensure order row exists before items reference it

        for pub_id, qty in cleaned:
            session.add(OrderItem(
                order_id=order_id,
                publication_id=pub_id,
                quantity=qty,
            ))

        session.commit()
        return order_id


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
def read_order(order_id):
    with Session(engine) as session:
        return session.get(Order, order_id)


def read_all_orders():
    with Session(engine) as session:
        return list(session.scalars(
            select(Order).order_by(Order.delivery_date, Order.id)
        ))


def read_order_items(order_id):
    """Return the OrderItem rows for one order, ordered by id."""
    with Session(engine) as session:
        return list(session.scalars(
            select(OrderItem)
            .where(OrderItem.order_id == order_id)
            .order_by(OrderItem.id)
        ))


def read_orders_by_customer(customer_id):
    """Return all orders for one customer, newest first."""
    with Session(engine) as session:
        return list(session.scalars(
            select(Order)
            .where(Order.customer_id == customer_id)
            .order_by(Order.delivery_date.desc())
        ))


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def update_order(order_id, customer_id, delivery_date, status, items):
    """Update order header and REPLACE its items.

    Items are replaced entirely: existing OrderItems for this order are
    deleted and re-inserted from the new list. This keeps total_amount
    consistent with the items.
    """
    # ---- validation ----
    if not isinstance(customer_id, int) or customer_id <= 0:
        return False
    if not _valid_date(delivery_date):
        return False
    if not _valid_status(status):
        return False

    with Session(engine) as session:
        order = session.get(Order, order_id)
        if order is None:
            return False

        if session.get(Customer, customer_id) is None:
            return False

        cleaned, prices = _validate_items(session, items)
        if cleaned is None:
            return False

        total = _compute_total(cleaned, prices)

        # Update header
        order.customer_id = customer_id
        order.delivery_date = delivery_date
        order.status = status
        order.total_amount = total

        # Replace items: delete existing, insert new
        # (delete-orphan cascade handles this if we clear the relationship,
        # but explicit delete is clearer)
        session.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).delete()

        for pub_id, qty in cleaned:
            session.add(OrderItem(
                order_id=order_id,
                publication_id=pub_id,
                quantity=qty,
            ))

        session.commit()
        return True


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def delete_order(order_id):
    """Delete the order and cascade-delete its items.

    The cascade='all, delete-orphan' on Order.items ensures the
    OrderItem rows go too.
    """
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if order is None:
            return False
        try:
            session.delete(order)
            session.commit()
            return True
        except IntegrityError:
            # Future-proof: if Billing gains an order_id FK later,
            # deleting an order referenced by a bill will fail here.
            session.rollback()
            return False
