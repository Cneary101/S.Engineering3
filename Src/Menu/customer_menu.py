# menus/customer_menu.py
"""Terminal menu for Customer CRUD. Phone is required (10 digits).

Wraps crud.customer.* with a numbered menu.
No login dependency — safe to test standalone:

    python -c "from menus.customer_menu import customer_menu; customer_menu()"
"""

from Customer.Customer import (
    create_customer,
    read_customer,
    read_all_customers,
    update_customer,
    delete_customer,
)
from Menu.helpers import (
    prompt_int,
    prompt_text,
    prompt_phone,
    prompt_yes_no,
)


def customer_menu():
    while True:
        choice = input(
            "\nCustomer Menu\n"
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
# Sub-handlers
# ---------------------------------------------------------------------------
def _create():
    customer_id = prompt_int("Customer ID: ")
    if customer_id is None:
        return

    name = prompt_text("First name: ")
    last_name = prompt_text("Last name: ")
    phone = prompt_phone("Phone (10 digits)")
    address = prompt_text("Address (optional): ", allow_empty=True) or None

    result = create_customer(customer_id, name, last_name, phone, address)
    if result is not False:
        print(f"Customer #{result} created.")
    else:
        print("Error: invalid details or duplicate ID.")


def _read():
    customer_id = prompt_int("Customer ID: ")
    if customer_id is None:
        return

    customer = read_customer(customer_id)
    if customer is None:
        print("Error: customer not found.")
        return
    _print_one(customer)


def _list_all():
    customers = read_all_customers()
    if not customers:
        print("No customers yet.")
        return
    for c in customers:
        _print_one(c)


def _update():
    customer_id = prompt_int("Customer ID: ")
    if customer_id is None:
        return

    customer = read_customer(customer_id)
    if customer is None:
        print("Error: customer not found.")
        return

    print(
        f"Current: {customer.name} {customer.last_name} | "
        f"phone={customer.phone} | address={customer.address or '-'}"
    )

    # Enter to keep; for address, '-' clears it.
    name = input(f"First name [{customer.name}]: ").strip() or customer.name
    last_name = (
        input(f"Last name [{customer.last_name}]: ").strip()
        or customer.last_name
    )
    phone = prompt_phone(
        "Phone", current=customer.phone, allow_blank_for_keep=True
    )

    raw_address = input(f"Address [{customer.address or '-'}]: ").strip()
    if raw_address == "":
        address = customer.address           # keep existing
    elif raw_address == "-":
        address = None                        # clear
    else:
        address = raw_address                 # set new

    if update_customer(customer_id, name, last_name, phone, address):
        print("Customer updated.")
    else:
        print("Error: invalid details. No changes made.")


def _delete():
    customer_id = prompt_int("Customer ID: ")
    if customer_id is None:
        return

    customer = read_customer(customer_id)
    if customer is None:
        print("Error: customer not found.")
        return

    if not prompt_yes_no(
        f"Delete {customer.name} {customer.last_name}? (y/n): "
    ):
        print("Cancelled.")
        return

    if delete_customer(customer_id):
        print("Customer deleted.")
    else:
        print(
            "Error: cannot delete — customer has orders or bills "
            "referencing them."
        )


# ---------------------------------------------------------------------------
# Display helper
# ---------------------------------------------------------------------------
def _print_one(c):
    print(
        f"#{c.id} | {c.name} {c.last_name} | "
        f"phone: {c.phone} | address: {c.address or '-'}"
    )