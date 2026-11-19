import re
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


from database import engine
from models import Customer

    #Verify methods to check value passes in correctly
def verify_id(value):
    return type(value) is int and value > 0

def verify_address(address):
    return address is None or isinstance(address, str)

def verify_name(name):
    # Letters, spaces, apostrophes and hyphens only, e.g. "Mary O'Brien", "Mary-Kate".
    # isalpha() also accepts accented letters such as "Seán".
    if not isinstance(name, str) or name.strip() == "":
        return False
    return all(char.isalpha() or char in " '-" for char in name.strip())


def verify_phone_number(phone_number):
    """Phone is REQUIRED: must be a string of exactly 10 digits."""
    if not isinstance(phone_number, str):
        return False
    return re.fullmatch(r"[0-9]{10}", phone_number) is not None


def _save(session):
    try:
        session.commit()
        return True
    except SQLAlchemyError:
        session.rollback()
        return False


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def create_customer(customer_id, name, last_name, phone, address):
    # ---- validation ----
    if not isinstance(customer_id, int) or customer_id <= 0:
        return False
    if not verify_name(name) or not verify_name(last_name):
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
        if not _save(session):
            return False
        return customer.id

# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
def read_customer(customer_id):
    if not verify_id(customer_id):
        return None
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
    if not verify_name(name) or not verify_name(last_name):
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
        session.add(customer)
        return _save(session)

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
        except SQLAlchemyError:
            session.rollback()
            return False

