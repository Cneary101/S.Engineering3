from datetime import date, timedelta

from sqlalchemy.orm import Session

from database import engine
from Login import LoginManager
from constants import (
    ORDER_PENDING, ORDER_CONFIRMED, ORDER_OUT_FOR_DELIVERY, ORDER_DELIVERED,
    ROUTE_PLANNED, ROUTE_IN_PROGRESS, ROUTE_COMPLETED,
    BILLING_UNPAID, BILLING_PAID, BILLING_OVERDUE,
    ROLE_ADMIN, ROLE_CLERK,
)
from models import (
    User, DeliveryArea, Customer, Publication,
    DeliveryPerson, Route, Order, OrderItem, Billing,
)


# ===========================================================================
# PRESERVED DATA — check-then-insert
# ===========================================================================
def seed_users(session):
    """Create default demo users if the user table is empty."""
    if session.query(User).first() is not None:
        print("Users already present — skipping user seed.")
        return

    lm = LoginManager(session)
    accounts = [
        ("admin1",  "1234", ROLE_ADMIN),
        ("clerk01", "5678", ROLE_CLERK),
        ("clerk02", "9012", ROLE_CLERK),
    ]
    created = []
    for username, password, role in accounts:
        if lm.create_user(username, password, role):
            created.append(username)
        else:
            print(f"  failed to create user '{username}'")

    if created:
        print(f"Seeded users: {', '.join(created)}")
        print("  Credentials: admin1/1234, clerk01/5678, clerk02/9012")


def seed_delivery_areas(session):
    """Create the five default areas if the area table is empty."""
    if session.query(DeliveryArea).first() is not None:
        print("Delivery areas already present — skipping area seed.")
        return

    for name in ("North", "South", "East", "West", "Central"):
        session.add(DeliveryArea(name=name))
    session.commit()
    print("Seeded 5 delivery areas.")


# ===========================================================================
# WIPE DEMO DATA — reverse-FK order
# ===========================================================================
def wipe_demo_data(session):
    """Delete demo data. Preserves users and delivery areas."""
    # Children before parents to respect FKs
    session.query(Billing).delete()
    session.query(OrderItem).delete()
    session.query(Order).delete()
    session.query(Route).delete()
    session.query(DeliveryPerson).delete()
    session.query(Publication).delete()
    session.query(Customer).delete()
    session.commit()
    print("Wiped: billings, order items, orders, routes, "
          "delivery persons, publications, customers.")


# ===========================================================================
# DEMO DATA — insert fresh
# ===========================================================================
def seed_customers(session):
    customers = [
        Customer(id=1, name="John",    last_name="Smith",   phone="5551234501", address="12 Main St, Dublin"),
        Customer(id=2, name="Jane",    last_name="Doe",     phone="5551234502", address="34 Elm Rd, Dublin"),
        Customer(id=3, name="Michael", last_name="O'Brien", phone="5551234503", address="56 Oak Ave, Cork"),
        Customer(id=4, name="Sarah",   last_name="Connor",  phone="5551234504", address="78 Pine Ln, Galway"),
        Customer(id=5, name="Ahmed",   last_name="Khan",    phone="5551234505", address="90 Cedar Dr, Dublin"),
        Customer(id=6, name="Emily",   last_name="Murphy",  phone="5551234506", address="11 Birch Way, Limerick"),
        Customer(id=7, name="Carlos",  last_name="Garcia",  phone="5551234507", address="22 Willow St, Cork"),
        Customer(id=8, name="Priya",   last_name="Patel",   phone="5551234508", address="33 Maple Ct, Galway"),
    ]
    session.add_all(customers)
    session.commit()
    print(f"Seeded {len(customers)} customers.")


def seed_publications(session):
    publications = [
        Publication(id=1, name="The Irish Times",     publication_type="newspaper", price=3.20, quantity=200),
        Publication(id=2, name="Irish Independent",   publication_type="newspaper", price=3.00, quantity=180),
        Publication(id=3, name="The Guardian",        publication_type="newspaper", price=3.50, quantity=150),
        Publication(id=4, name="Time",                publication_type="magazine",  price=5.50, quantity=80),
        Publication(id=5, name="National Geographic", publication_type="magazine",  price=6.50, quantity=60),
        Publication(id=6, name="The Economist",       publication_type="magazine",  price=7.00, quantity=45),
        Publication(id=7, name="The Sun",             publication_type="tabloid",   price=1.50, quantity=250),
        Publication(id=8, name="Daily Mirror",        publication_type="tabloid",   price=1.80, quantity=4),
    ]
    session.add_all(publications)
    session.commit()
    print(f"Seeded {len(publications)} publications "
          f"(note: Daily Mirror is low-stock on purpose).")


def seed_delivery_persons(session):
    # Look up area IDs by name — survives any ID scheme
    area_map = {a.name: a.id for a in session.query(DeliveryArea).all()}
    persons = [
        DeliveryPerson(id=1, name="Pat Murphy",   area_id=area_map["North"]),
        DeliveryPerson(id=2, name="Maria Garcia", area_id=area_map["South"]),
        DeliveryPerson(id=3, name="Tom Kelly",    area_id=area_map["East"]),
        DeliveryPerson(id=4, name="Aisha Bello",  area_id=area_map["West"]),
    ]
    session.add_all(persons)
    session.commit()
    print(f"Seeded {len(persons)} delivery persons.")


def seed_routes(session):
    today = date.today()
    routes = [
        Route(id=1, date=today - timedelta(days=2), driver_id=1, status=ROUTE_COMPLETED),
        Route(id=2, date=today,                     driver_id=2, status=ROUTE_IN_PROGRESS),
        Route(id=3, date=today + timedelta(days=1), driver_id=3, status=ROUTE_PLANNED),
        Route(id=4, date=today + timedelta(days=2), driver_id=4, status=ROUTE_PLANNED),
    ]
    session.add_all(routes)
    session.commit()
    print(f"Seeded {len(routes)} routes.")


def seed_orders(session):
    """Create orders with items. Each order's total_amount is computed."""
    today = date.today()

    # Look up publication IDs by name — survives any ID scheme
    pub_map = {p.name: p for p in session.query(Publication).all()}

    # (order_id, customer_id, delivery_offset_days, status, [(pub_name, qty), ...])
    order_specs = [
        (1,  1, 0, ORDER_DELIVERED,        [("The Irish Times", 2), ("The Sun", 1)]),
        (2,  2, 0, ORDER_OUT_FOR_DELIVERY, [("Irish Independent", 1), ("The Guardian", 1)]),
        (3,  3, 1, ORDER_CONFIRMED,        [("The Irish Times", 1)]),
        (4,  4, 1, ORDER_CONFIRMED,        [("Time", 1), ("National Geographic", 1)]),
        (5,  5, 2, ORDER_PENDING,          [("The Economist", 1)]),
        (6,  6, 2, ORDER_PENDING,          [("The Sun", 3)]),
        (7,  7, 0, ORDER_DELIVERED,        [("Irish Independent", 2), ("Daily Mirror", 2)]),
        (8,  8, 3, ORDER_PENDING,          [("The Guardian", 1), ("Time", 1), ("The Sun", 1)]),
        (9,  1, 3, ORDER_CONFIRMED,        [("National Geographic", 1)]),
        (10, 2, 5, ORDER_PENDING,          [("The Irish Times", 1), ("The Economist", 1)]),
    ]

    orders_created = 0
    items_created = 0

    for order_id, cust_id, offset, status, items in order_specs:
        # Compute total from current publication prices
        total = sum(pub_map[pname].price * qty for pname, qty in items)

        order = Order(
            id=order_id,
            customer_id=cust_id,
            delivery_date=today + timedelta(days=offset),
            status=status,
            total_amount=float(total),
        )
        session.add(order)
        session.flush()  # ensure order row exists before inserting items

        for pub_name, qty in items:
            session.add(OrderItem(
                order_id=order_id,
                publication_id=pub_map[pub_name].id,
                quantity=qty,
            ))
            items_created += 1

        orders_created += 1

    session.commit()
    print(f"Seeded {orders_created} orders with {items_created} order items.")


def seed_billings(session):
    today = date.today()
    billings = [
        Billing(id=1, customer_id=1, amount=8.20,  status=BILLING_PAID,    due_date=today - timedelta(days=15)),
        Billing(id=2, customer_id=2, amount=6.50,  status=BILLING_PAID,    due_date=today - timedelta(days=10)),
        Billing(id=3, customer_id=3, amount=3.20,  status=BILLING_OVERDUE, due_date=today - timedelta(days=5)),
        Billing(id=4, customer_id=4, amount=12.00, status=BILLING_UNPAID,  due_date=today + timedelta(days=7)),
        Billing(id=5, customer_id=5, amount=7.00,  status=BILLING_UNPAID,  due_date=today + timedelta(days=14)),
        Billing(id=6, customer_id=1, amount=3.50,  status=BILLING_UNPAID,  due_date=today + timedelta(days=21)),
    ]
    session.add_all(billings)
    session.commit()
    print(f"Seeded {len(billings)} billings.")


# ===========================================================================
# MAIN
# ===========================================================================
def main():
    with Session(engine) as session:
        # Preserved data
        seed_users(session)
        seed_delivery_areas(session)

        # Deterministic demo data
        wipe_demo_data(session)
        seed_customers(session)
        seed_publications(session)
        seed_delivery_persons(session)
        seed_routes(session)
        seed_orders(session)
        seed_billings(session)

    print("\n✓ Seed complete.")


if __name__ == "__main__":
    main()