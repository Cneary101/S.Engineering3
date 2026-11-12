from Publications.Publication import (
    create_publication,
    read_publication,
    read_all_publications,
    update_publication,
    delete_publication,
    verify_low_stock,
)
from Menu.helpers import (
    prompt_int,
    prompt_text,
    prompt_yes_no,
)


def publication_menu():
    while True:
        choice = input(
            "\nPublication Menu\n"
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
    publication_id = prompt_int("Publication ID: ")
    if publication_id is None:
        return

    name = prompt_text("Name: ")
    publication_type = prompt_text("Type (e.g. newspaper, magazine): ")
    price = _prompt_price("Price")
    if price is None:
        return
    quantity = prompt_int("Quantity in stock: ")
    if quantity is None:
        return

    result = create_publication(publication_id, name, publication_type, price, quantity)
    if result is not False:
        print(f"Publication #{result} created.")
    else:
        print("Error: invalid details or duplicate ID.")


def _read():
    publication_id = prompt_int("Publication ID: ")
    if publication_id is None:
        return

    publication = read_publication(publication_id)
    if publication is None:
        print("Error: publication not found.")
        return
    _print_one(publication)
    if verify_low_stock(publication):
        print("Warning: low stock (5 or fewer copies).")


def _list_all():
    publications = read_all_publications()
    if not publications:
        print("No publications yet.")
        return
    for p in publications:
        _print_one(p)


def _update():
    publication_id = prompt_int("Publication ID: ")
    if publication_id is None:
        return

    publication = read_publication(publication_id)
    if publication is None:
        print("Error: publication not found.")
        return

    print(
        f"Current: {publication.name} | type={publication.publication_type} | "
        f"price={publication.price} | quantity={publication.quantity}"
    )

    name = input(f"Name [{publication.name}]: ").strip() or publication.name
    ptype = (
        input(f"Type [{publication.publication_type}]: ").strip()
        or publication.publication_type
    )

    raw_price = input(f"Price [{publication.price}]: ").strip()
    if raw_price == "":
        price = float(publication.price)
    else:
        try:
            price = float(raw_price)
        except ValueError:
            print("Error: invalid price. No changes made.")
            return

    raw_qty = input(f"Quantity [{publication.quantity}]: ").strip()
    if raw_qty == "":
        quantity = publication.quantity
    else:
        try:
            quantity = int(raw_qty)
        except ValueError:
            print("Error: invalid quantity. No changes made.")
            return

    if update_publication(publication_id, name, ptype, price, quantity):
        print("Publication updated.")
    else:
        print("Error: invalid details. No changes made.")


def _delete():
    publication_id = prompt_int("Publication ID: ")
    if publication_id is None:
        return

    publication = read_publication(publication_id)
    if publication is None:
        print("Error: publication not found.")
        return

    if not prompt_yes_no(
        f"Delete {publication.name} (ID {publication.id})? (y/n): "
    ):
        print("Cancelled.")
        return

    if delete_publication(publication_id):
        print("Publication deleted.")
    else:
        print(
            "Error: cannot delete — publication is referenced by "
            "one or more order items."
        )


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------
def _print_one(p):
    print(
        f"#{p.id} | {p.name} | type: {p.publication_type} | "
        f"price: {p.price} | stock: {p.quantity}"
    )


def _prompt_price(prompt):
    """Prompt until a valid non-negative number is entered. Returns float or None."""
    while True:
        raw = input(f"{prompt}: ").strip()
        try:
            value = float(raw)
        except ValueError:
            print("Error: enter a number.")
            return None
        if value < 0:
            print("Error: price cannot be negative.")
            continue
        return value