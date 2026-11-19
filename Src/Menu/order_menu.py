from datetime import date as date_type

from Billing.Billing import print_bill_for_order
from constants import ORDER_STATUSES
from Customer.Customer import (
    read_all_customers,
    read_customer,
)
from Menu.helpers import (
    prompt_int,
    prompt_yes_no,
)
from Order import (
    create_order,
    read_order,
    read_all_orders,
    read_order_items,
    update_order,
    delete_order,
)
from Publications.Publication import (
    read_all_publications,
    read_publication,
)


def order_menu():
    while True:
        choice = input(
            "\nOrder Menu\n"
            "1: Create\n"
            "2: Read (by ID)\n"
            "3: List all\n"
            "4: Update\n"
            "5: Delete\n"
            "6: Back\n"
            "Choice: "
        ).strip()

        if choice == "1":
            _create()
        elif choice == "2":
            _read()
        elif choice == "3":
            _list_all()
        elif choice == "4":
            _update()
        elif choice == "5":
            _delete()
        elif choice == "6":
            return
        else:
            print("Error: invalid choice.")


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def _create():
    order_id = prompt_int("Order ID: ")
    if order_id is None:
        return

    customer_id = _pick_customer()
    if customer_id is None:
        print("Cancelled.")
        return

    delivery_date = _prompt_date()
    if delivery_date is None:
        print("Cancelled.")
        return

    status = _pick_status()
    if status is None:
        print("Cancelled.")
        return

    items = _collect_items()
    if items is None:
        print("Cancelled.")
        return

    _preview(items)
    if not prompt_yes_no("Confirm and save? (y/n): "):
        print("Cancelled.")
        return

    result = create_order(order_id, customer_id, delivery_date, status, items)
    if result is not False:
        print(f"Order #{result} created.")
        if prompt_yes_no("Generate bill for this order? (y/n): "):
            _bill_order(result)
    else:
        print("Error: invalid details, duplicate ID, or unknown reference.")


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
def _read():
    order_id = prompt_int("Order ID: ")
    if order_id is None:
        return

    order = read_order(order_id)
    if order is None:
        print("Error: order not found.")
        return
    _print_order(order)
    if order.status != "cancelled":
        if prompt_yes_no("Generate bill for this order? (y/n): "):
            _bill_order(order_id)


# ---------------------------------------------------------------------------
# List all
# ---------------------------------------------------------------------------
def _list_all():
    orders = read_all_orders()
    if not orders:
        print("No orders yet.")
        return
    for o in orders:
        _print_summary(o)


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def _update():
    order_id = prompt_int("Order ID: ")
    if order_id is None:
        return

    order = read_order(order_id)
    if order is None:
        print("Error: order not found.")
        return

    _print_order(order)

    # ----- customer -----
    if prompt_yes_no("Change customer? (y/n): "):
        customer_id = _pick_customer()
        if customer_id is None:
            print("Cancelled.")
            return
    else:
        customer_id = order.customer_id

    # ----- delivery date -----
    raw = input(
        f"Delivery date [{order.delivery_date}] (YYYY-MM-DD, Enter to keep): "
    ).strip()
    if raw == "":
        delivery_date = order.delivery_date
    else:
        try:
            delivery_date = date_type.fromisoformat(raw)
        except ValueError:
            print("Error: date must be YYYY-MM-DD. No changes made.")
            return

    # ----- status -----
    print(f"Current status: {order.status}")
    if prompt_yes_no("Change status? (y/n): "):
        status = _pick_status()
        if status is None:
            print("Cancelled.")
            return
    else:
        status = order.status

    # ----- items -----
    if prompt_yes_no("Replace items? (y/n): "):
        items = _collect_items()
        if items is None:
            print("Cancelled.")
            return
    else:
        existing = read_order_items(order_id)
        items = [(item.publication_id, item.quantity) for item in existing]
        if not items:
            print("Error: order has no items. Cannot keep empty item list.")
            return

    _preview(items)
    if not prompt_yes_no("Confirm and save? (y/n): "):
        print("Cancelled.")
        return

    if update_order(order_id, customer_id, delivery_date, status, items):
        print("Order updated.")
    else:
        print("Error: invalid details. No changes made.")


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def _delete():
    order_id = prompt_int("Order ID: ")
    if order_id is None:
        return

    order = read_order(order_id)
    if order is None:
        print("Error: order not found.")
        return

    _print_order(order)

    if not prompt_yes_no(
        f"Delete Order #{order.id} and all its items? (y/n): "
    ):
        print("Cancelled.")
        return

    if delete_order(order_id):
        print("Order deleted.")
    else:
        print("Error: could not delete order.")


# ---------------------------------------------------------------------------
# Pickers
# ---------------------------------------------------------------------------
def _pick_customer():
    """Numbered list of customers; returns customer_id or None."""
    customers = read_all_customers()
    if not customers:
        print("Error: no customers exist. Create one first.")
        return None

    print("\nAvailable customers:")
    for idx, c in enumerate(customers, start=1):
        print(f"  {idx}: {c.name} {c.last_name} (ID {c.id})")

    while True:
        raw = input(
            f"Choose customer (1-{len(customers)}), or 0 to cancel: "
        ).strip()
        try:
            n = int(raw)
        except ValueError:
            print("Error: enter a number.")
            continue
        if n == 0:
            return None
        if 1 <= n <= len(customers):
            return customers[n - 1].id
        print(f"Error: enter a number between 1 and {len(customers)}.")


def _pick_status():
    """Numbered list of statuses; returns selected string or None."""
    print("\nAvailable statuses:")
    for idx, status in enumerate(ORDER_STATUSES, start=1):
        print(f"  {idx}: {status}")

    while True:
        raw = input(
            f"Choose status (1-{len(ORDER_STATUSES)}), or 0 to cancel: "
        ).strip()
        try:
            n = int(raw)
        except ValueError:
            print("Error: enter a number.")
            continue
        if n == 0:
            return None
        if 1 <= n <= len(ORDER_STATUSES):
            return ORDER_STATUSES[n - 1]
        print(f"Error: enter a number between 1 and {len(ORDER_STATUSES)}.")


def _pick_publication():
    """Numbered list of publications; returns pub_id or None."""
    publications = read_all_publications()
    if not publications:
        print("Error: no publications exist. Create one first.")
        return None

    print("\nAvailable publications:")
    for idx, p in enumerate(publications, start=1):
        print(f"  {idx}: {p.name} ({p.publication_type}) — €{p.price}")

    while True:
        raw = input(
            f"Choose publication (1-{len(publications)}), or 0 to cancel: "
        ).strip()
        try:
            n = int(raw)
        except ValueError:
            print("Error: enter a number.")
            continue
        if n == 0:
            return None
        if 1 <= n <= len(publications):
            return publications[n - 1].id
        print(f"Error: enter a number between 1 and {len(publications)}.")


def _prompt_date():
    raw = input("Delivery date (YYYY-MM-DD): ").strip()
    try:
        return date_type.fromisoformat(raw)
    except ValueError:
        print("Error: date must be in YYYY-MM-DD format.")
        return None


# ---------------------------------------------------------------------------
# Item-entry sub-loop
# ---------------------------------------------------------------------------
def _collect_items():
    """Loop: pick publication → quantity → add another?

    Duplicates are merged (same publication picked twice → summed quantity).
    Returns list of (pub_id, qty) tuples, or None if cancelled before any item.
    """
    items = {}
    while True:
        pub_id = _pick_publication()
        if pub_id is None:
            # Cancelled or no publications exist
            return list(items.items()) if items else None

        qty = prompt_int("Quantity: ")
        if qty is None or qty <= 0:
            print("Error: quantity must be a positive whole number.")
            continue

        items[pub_id] = items.get(pub_id, 0) + qty
        print(f"  → added: publication {pub_id} × {qty} "
              f"(total for this pub: {items[pub_id]})")

        if not prompt_yes_no("Add another item? (y/n): "):
            break

    return list(items.items()) if items else None


# ---------------------------------------------------------------------------
# Billing
# ---------------------------------------------------------------------------
def _bill_order(order_id):
    """Generate and print a bill for the given order."""
    result = print_bill_for_order(order_id)
    if result is not False:
        print(f"Bill #{result} created.")
    else:
        print("Bill generation failed.")


# ---------------------------------------------------------------------------
# Preview / display helpers
# ---------------------------------------------------------------------------
def _preview(items):
    """Show items and computed subtotal BEFORE commit."""
    print("\n  Preview:")
    total = 0.0
    for pub_id, qty in items:
        pub = read_publication(pub_id)
        if pub is None:
            print(f"    publication {pub_id} × {qty}  (missing!)")
            continue
        line = float(pub.price) * qty
        total += line
        print(f"    {pub.name} × {qty}  = {line:.2f}")
    print(f"  → estimated total: {total:.2f}")


def _print_order(order):
    """Full detail: header + items."""
    customer = read_customer(order.customer_id)
    cust_name = (
        f"{customer.name} {customer.last_name}" if customer
        else f"#{order.customer_id}"
    )
    print(
        f"\nOrder #{order.id}\n"
        f"  Customer: {cust_name}\n"
        f"  Delivery: {order.delivery_date}\n"
        f"  Status:   {order.status}\n"
        f"  Total:    {order.total_amount:.2f}\n"
        f"  Items:"
    )
    for item in read_order_items(order.id):
        pub = read_publication(item.publication_id)
        pub_name = pub.name if pub else f"#{item.publication_id}"
        print(f"    {pub_name} × {item.quantity}")


def _print_summary(order):
    """One-line summary for list view."""
    customer = read_customer(order.customer_id)
    cust_name = (
        f"{customer.name} {customer.last_name}" if customer
        else f"#{order.customer_id}"
    )
    items = read_order_items(order.id)
    print(
        f"#{order.id} | {cust_name} | {order.delivery_date} | "
        f"{order.status} | {order.total_amount:.2f} | {len(items)} item(s)"
    )
