from DeliveryArea import read_all_areas, read_area
from DeliveryPerson import (
    create_delivery_person,
    read_delivery_person,
    read_all_delivery_persons,
    update_delivery_person,
    delete_delivery_person,
)
from Menu.helpers import (
    prompt_int,
    prompt_text,
    prompt_yes_no,
)


def delivery_person_menu():
    while True:
        choice = input(
            "\nDelivery Person Menu\n"
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
    person_id = prompt_int("Delivery Person ID: ")
    if person_id is None:
        return

    name = prompt_text("Name: ")
    area_id = _pick_area()
    if area_id is None:
        print("Cancelled.")
        return

    result = create_delivery_person(person_id, name, area_id)
    if result is not False:
        print(f"Delivery Person #{result} created.")
    else:
        print("Error: invalid details, duplicate ID, or unknown area.")


def _read():
    person_id = prompt_int("Delivery Person ID: ")
    if person_id is None:
        return

    person = read_delivery_person(person_id)
    if person is None:
        print("Error: delivery person not found.")
        return
    _print_one(person)


def _list_all():
    persons = read_all_delivery_persons()
    if not persons:
        print("No delivery persons yet.")
        return
    for p in persons:
        _print_one(p)


def _update():
    person_id = prompt_int("Delivery Person ID: ")
    if person_id is None:
        return

    person = read_delivery_person(person_id)
    if person is None:
        print("Error: delivery person not found.")
        return

    current_area = read_area(person.area_id)
    area_name = current_area.name if current_area else f"#{person.area_id}"
    print(f"Current: {person.name} | area: {area_name}")

    name = input(f"Name [{person.name}]: ").strip() or person.name

    print("Change area?")
    if prompt_yes_no("Pick a new area? (y/n): "):
        area_id = _pick_area()
        if area_id is None:
            print("Cancelled.")
            return
    else:
        area_id = person.area_id

    if update_delivery_person(person_id, name, area_id):
        print("Delivery Person updated.")
    else:
        print("Error: invalid details or unknown area. No changes made.")


def _delete():
    person_id = prompt_int("Delivery Person ID: ")
    if person_id is None:
        return

    person = read_delivery_person(person_id)
    if person is None:
        print("Error: delivery person not found.")
        return

    if not prompt_yes_no(
        f"Delete {person.name} (ID {person.id})? (y/n): "
    ):
        print("Cancelled.")
        return

    if delete_delivery_person(person_id):
        print("Delivery Person deleted.")
    else:
        print(
            "Error: cannot delete — this delivery person has routes "
            "assigned and cannot be removed."
        )


# ---------------------------------------------------------------------------
# Area picker
# ---------------------------------------------------------------------------
def _pick_area():
    """Show numbered list of areas; return the chosen area_id, or None."""
    areas = read_all_areas()
    if not areas:
        print("Error: no delivery areas exist. Run seed.py first.")
        return None

    print("\nAvailable areas:")
    for idx, area in enumerate(areas, start=1):
        print(f"  {idx}: {area.name}")

    while True:
        raw = input(f"Choose area (1-{len(areas)}), or 0 to cancel: ").strip()
        try:
            n = int(raw)
        except ValueError:
            print("Error: enter a number.")
            continue
        if n == 0:
            return None
        if 1 <= n <= len(areas):
            return areas[n - 1].id
        print(f"Error: enter a number between 1 and {len(areas)}, or 0 to cancel.")


# ---------------------------------------------------------------------------
# Display helper
# ---------------------------------------------------------------------------
def _print_one(p):
    area = read_area(p.area_id)
    area_name = area.name if area else f"#{p.area_id}"
    print(f"#{p.id} | {p.name} | area: {area_name}")