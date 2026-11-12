import re
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import engine
from models import Customer

    #Verify methods to check value passes in correctly
def verify_text(value):
    return isinstance(value, str) and value.strip() != ""


def verify_phone_number(phone_number):
    """Phone is REQUIRED: must be a string of exactly 10 digits."""
    if not isinstance(phone_number, str):
        return False
    return re.fullmatch(r"[0-9]{10}", phone_number) is not None
# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def create_customer(customer_id, name, last_name, phone, address):
    # ---- validation ----
    if not isinstance(customer_id, int) or customer_id <= 0:
        return False
    if not verify_text(name) or not verify_text(last_name):
        return False
    if not verify_phone_number(phone):
        return False

    # ---- persist ----
    with Session(engine) as session:
        if session.get(Customer, customer_id) is not None:
            return False  # duplicate ID

        customer = Customer(
            id=customer_id,
            name=name.strip(),
            last_name=last_name.strip(),
            phone=phone.strip(),                       # required — no None branch
            address=address.strip() if address else None,   # address still optional
        )
        session.add(customer)
        session.commit()
        return customer_id

# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
def read_customer(customer_id):
    with Session(engine) as session:
        return session.get(Customer, customer_id)


def read_all_customers():
    with Session(engine) as session:
        return list(session.scalars(select(Customer).order_by(Customer.id)))


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def update_customer(customer_id, name, last_name, phone, address):
    # ---- validation ----
    if not verify_text(name) or not verify_text(last_name):
        return False
    if not verify_phone_number(phone):
        return False

    with Session(engine) as session:
        customer = session.get(Customer, customer_id)
        if customer is None:
            return False

        customer.name = name.strip()
        customer.last_name = last_name.strip()
        customer.phone = phone.strip()                     # required
        customer.address = address.strip() if address else None
        session.commit()
        return True

# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def delete_customer(customer_id):
    with Session(engine) as session:
        customer = session.get(Customer, customer_id)
        if customer is None:
            return False
        try:
            session.delete(customer)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False

