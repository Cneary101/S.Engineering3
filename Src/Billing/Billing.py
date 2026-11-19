from datetime import date as date_type, timedelta

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from constants import BILLING_STATUSES, BILLING_UNPAID
from database import engine
from models import Billing, Order, OrderItem, Customer, Publication


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------
def _valid_date(value):
    return isinstance(value, date_type)


def _valid_status(value):
    return isinstance(value, str) and value in BILLING_STATUSES


def _valid_amount(value):
    return isinstance(value, (int, float)) and value >= 0


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def create_billing(billing_id, customer_id, amount, status, due_date):
    """Insert a single Billing row. Returns billing_id or False."""
    if not isinstance(billing_id, int) or billing_id <= 0:
        return False
    if not isinstance(customer_id, int) or customer_id <= 0:
        return False
    if not _valid_amount(amount):
        return False
    if not _valid_status(status):
        return False
    if not _valid_date(due_date):
        return False

    with Session(engine) as session:
        if session.get(Billing, billing_id) is not None:
            return False  # duplicate ID
        if session.get(Customer, customer_id) is None:
            return False  # FK target missing

        bill = Billing(
            id=billing_id,
            customer_id=customer_id,
            amount=float(amount),
            status=status,
            due_date=due_date,
        )
        session.add(bill)
        session.commit()
        return billing_id


def next_billing_id():
    """Return max(billing.id) + 1, or 1 if the table is empty."""
    with Session(engine) as session:
        current_max = session.scalar(select(func.max(Billing.id))) or 0
        return int(current_max) + 1


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
def read_billing(billing_id):
    with Session(engine) as session:
        return session.get(Billing, billing_id)


def read_all_billings():
    with Session(engine) as session:
        return list(session.scalars(
            select(Billing).order_by(Billing.due_date, Billing.id)
        ))


def read_billings_by_customer(customer_id):
    """Return all bills for one customer, newest due date first."""
    with Session(engine) as session:
        return list(session.scalars(
            select(Billing)
            .where(Billing.customer_id == customer_id)
            .order_by(Billing.due_date.desc())
        ))


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def update_billing(billing_id, customer_id, amount, status, due_date):
    """Update an existing bill. Returns True or False.

    All fields are required (no partial update); the menu is responsible
    for resending unchanged fields.
    """
    if not isinstance(customer_id, int) or customer_id <= 0:
        return False
    if not _valid_amount(amount):
        return False
    if not _valid_status(status):
        return False
    if not _valid_date(due_date):
        return False

    with Session(engine) as session:
        bill = session.get(Billing, billing_id)
        if bill is None:
            return False
        if session.get(Customer, customer_id) is None:
            return False

        bill.customer_id = customer_id
        bill.amount = float(amount)
        bill.status = status
        bill.due_date = due_date
        session.commit()
        return True


def mark_billing_paid(billing_id):
    """Convenience: flip a bill's status to 'paid'. Returns True/False."""
    with Session(engine) as session:
        bill = session.get(Billing, billing_id)
        if bill is None:
            return False
        bill.status = "paid"
        session.commit()
        return True


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def delete_billing(billing_id):
    with Session(engine) as session:
        bill = session.get(Billing, billing_id)
        if bill is None:
            return False
        try:
            session.delete(bill)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False


# ---------------------------------------------------------------------------
# High-level: bill an order + print invoice
# ---------------------------------------------------------------------------
def print_bill_for_order(order_id, due_offset_days=30):
    """Generate a bill for the given order and print an invoice.

    - Reads the order, its items, and the customer
    - Computes the total (using current publication prices)
    - Inserts a Billing row with status='unpaid'
    - Prints a formatted invoice to the terminal

    Returns the new billing_id on success, False on failure.

    Important: all ORM data is snapshotted into plain Python BEFORE the
    session closes, to avoid DetachedInstanceError during printing.
    """
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if order is None:
            print("Error: order not found.")
            return False

        if order.status == "cancelled":
            print("Error: cannot bill a cancelled order.")
            return False

        customer = session.get(Customer, order.customer_id)
        if customer is None:
            print("Error: customer not found for this order.")
            return False

        items = session.scalars(
            select(OrderItem).where(OrderItem.order_id == order_id)
        ).all()

        if not items:
            print("Error: order has no items — cannot generate bill.")
            return False

        pub_ids = [item.publication_id for item in items]
        publications = {
            p.id: p for p in session.scalars(
                select(Publication).where(Publication.id.in_(pub_ids))
            ).all()
        }

        # ---- compute line rows and total from current prices ----
        total = 0.0
        line_rows = []
        for item in items:
            pub = publications.get(item.publication_id)
            if pub is None:
                print(f"Warning: publication {item.publication_id} "
                      f"not found — skipping line.")
                continue
            unit_price = float(pub.price)
            line_total = unit_price * item.quantity
            total += line_total
            line_rows.append((pub.name, item.quantity, unit_price, line_total))

        if not line_rows:
            print("Error: no valid line items — cannot generate bill.")
            return False

        # ---- allocate bill id and insert row ----
        current_max = session.scalar(select(func.max(Billing.id))) or 0
        bill_id = int(current_max) + 1

        due_date = order.delivery_date + timedelta(days=due_offset_days)

        bill = Billing(
            id=bill_id,
            customer_id=customer.id,
            amount=round(total, 2),
            status=BILLING_UNPAID,
            due_date=due_date,
        )
        session.add(bill)
        session.commit()

        # ---- SNAPSHOT into plain Python BEFORE session closes ----
        customer_info = {
            "name":      customer.name,
            "last_name": customer.last_name,
            "address":   customer.address,
            "phone":     customer.phone,
        }
        order_info = {
            "id":            order.id,
            "delivery_date": order.delivery_date,
        }

    # ---- print invoice OUTSIDE the session — only plain data ----
    _print_invoice(
        bill_id=bill_id,
        customer_info=customer_info,
        order_info=order_info,
        line_rows=line_rows,
        total=total,
        due_date=due_date,
    )

    return bill_id


# ---------------------------------------------------------------------------
# Invoice printing
# ---------------------------------------------------------------------------
def _print_invoice(bill_id, customer_info, order_info, line_rows, total, due_date):
    line = "-" * 60
    print()
    print(line)
    print(f"  INVOICE #{bill_id}")
    print(line)
    print(f"  Customer:  {customer_info['name']} {customer_info['last_name']}")
    print(f"  Address:   {customer_info['address'] or '-'}")
    print(f"  Phone:     {customer_info['phone']}")
    print(f"  Order #:   {order_info['id']}")
    print(f"  Delivery:  {order_info['delivery_date']}")
    print(f"  Due date:  {due_date}")
    print(line)
    print(f"  {'Publication':<30} {'Qty':>5} {'Unit':>8} {'Line':>10}")
    print(line)
    for name, qty, unit, line_total in line_rows:
        print(f"  {name:<30} {qty:>5} {unit:>8.2f} {line_total:>10.2f}")
    print(line)
    print(f"  {'TOTAL':<30} {'':>5} {'':>8} {total:>10.2f}")
    print(line)
    print(f"  Status:    UNPAID")
    print(f"  Bill ID:   {bill_id}")
    print(line)
    print()