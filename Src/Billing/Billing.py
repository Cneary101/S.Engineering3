from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import engine
from models import Billing, Customer, Order, OrderItem, Publication


def verify_id(value):
    return type(value) is int and value > 0


def verify_month(month):
    if not isinstance(month, str) or len(month) != 7:
        return False
    try:
        return date.fromisoformat(month + "-01").strftime("%Y-%m") == month
    except ValueError:
        return False


def verify_due_date(due_date):
    if due_date is None or isinstance(due_date, date):
        return True
    if isinstance(due_date, str):
        try:
            date.fromisoformat(due_date)
            return True
        except ValueError:
            pass
    return False


def _as_date(due_date):
    return date.fromisoformat(due_date) if isinstance(due_date, str) else due_date


def _calculate_total(session, customer_id, month):
    year, month_number = map(int, month.split("-"))
    start = date(year, month_number, 1)
    end = date(year + 1, 1, 1) if month_number == 12 else date(year, month_number + 1, 1)

    rows = session.execute(
        select(Publication.price, OrderItem.quantity)
        .join(OrderItem, OrderItem.publication_id)
        .join(Order, OrderItem.order_id)
        .where(Order.customer_id,
               Order.delivery_date >= start,
               Order.delivery_date < end,
               Order.status.in_(("Delivered", "Completed")))
    ).all()
    return sum((Decimal(price) * quantity for price, quantity in rows), Decimal("0.00"))


def calculate_total(customer_id, month):
    if not verify_id(customer_id) or not verify_month(month):
        return None
    with Session(engine) as session:
        return _calculate_total(session, customer_id, month)


# Create
# New bills start as drafts; their total comes from delivered SQL orders.
def create_bill(bill_id, customer_id, month, due_date=None):
    if not verify_id(bill_id) or not verify_id(customer_id):
        return False
    if not verify_month(month) or not verify_due_date(due_date):
        return False

    with Session(engine) as session:
        if session.get(Billing, bill_id) is not None:
            return False
        if session.get(Customer, customer_id) is None:
            return False
        bill = Billing(id=bill_id, customer_id=customer_id, month=month,
                       amount=_calculate_total(session, customer_id, month),
                       status="Draft", due_date=_as_date(due_date))
        session.add(bill)
        try:
            session.commit()
            return bill_id
        except IntegrityError:
            session.rollback()
            return False


# Read
def read_bill(bill_id):
    with Session(engine) as session:
        return session.get(Billing, bill_id)


def read_all_bills():
    with Session(engine) as session:
        return list(session.scalars(select(Billing).order_by(Billing.id)))


# Update
# Only draft bills can be recalculated or changed.
def update_bill(bill_id, customer_id, month):
    if not verify_id(customer_id) or not verify_month(month):
        return False
    with Session(engine) as session:
        bill = session.get(Billing, bill_id)
        if bill is None or bill.status != "Draft":
            return False
        if session.get(Customer, customer_id) is None:
            return False
        bill.customer_id = customer_id
        bill.month = month
        bill.amount = _calculate_total(session, customer_id, month)
        session.commit()
        return True


def update_bill_status(bill_id, status, due_date=None):
    if status not in ("Issued", "Paid") or not verify_due_date(due_date):
        return False
    with Session(engine) as session:
        bill = session.get(Billing, bill_id)
        if bill is None:
            return False
        if (bill.status, status) not in (("Draft", "Issued"), ("Issued", "Paid")):
            return False
        if due_date is not None:
            bill.due_date = _as_date(due_date)
        bill.status = status
        session.commit()
        return True


# Delete
# Issued or paid bills cannot be deleted.
def delete_bill(bill_id):
    with Session(engine) as session:
        bill = session.get(Billing, bill_id)
        if bill is None or bill.status != "Draft":
            return False
        try:
            session.delete(bill)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False
