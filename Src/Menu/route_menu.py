from datetime import date as date_type

from constants import ROUTE_STATUSES
from DeliveryPerson import (
    read_all_delivery_persons,
    read_delivery_person,
)
from Menu.helpers import (
    prompt_int,
    prompt_yes_no,
)
from Route import (
    create_route,
    read_route,
    read_all_routes,
    update_route,
    delete_route,
)


def docket_menu():
    while True:
        choice = input(
            "\nDelivery Docket (Route) Menu\n"
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
    route_id = prompt_int("Route ID: ")
    if route_id is None:
        return

    route_date = _prompt_date()
    if route_date is None:
        print("Cancelled.")
        return

    driver_id = _pick_driver()
    if driver_id is None:
        print("Cancelled.")
        return

    status = _pick_status()
    if status is None:
        print("Cancelled.")
        return

    result = create_route(route_id, route_date, driver_id, status)
    if result is not False:
        print(f"Route #{result} created.")
    else:
        print("Error: invalid details, duplicate ID, or unknown driver.")


def _read():
    route_id = prompt_int("Route ID: ")
    if route_id is None:
        return

    route = read_route(route_id)
    if route is None:
        print("Error: route not found.")
        return
    _print_one(route)


def _list_all():
    routes = read_all_routes()
    if not routes:
        print("No routes yet.")
        return
    for r in routes:
        _print_one(r)


def _update():
    route_id = prompt_int("Route ID: ")
    if route_id is None:
        return

    route = read_route(route_id)
    if route is None:
        print("Error: route not found.")
        return

    driver = read_delivery_person(route.driver_id)
    driver_name = driver.name if driver else f"#{route.driver_id}"
    print(
        f"Current: date={route.date} | driver={driver_name} | "
        f"status={route.status}"
    )

    # Date
    raw = input(f"Date [{route.date}] (YYYY-MM-DD, Enter to keep): ").strip()
    if raw == "":
        route_date = route.date
    else:
        try:
            route_date = date_type.fromisoformat(raw)
        except ValueError:
            print("Error: date must be YYYY-MM-DD. No changes made.")
            return

    # Driver
    if prompt_yes_no("Change driver? (y/n): "):
        driver_id = _pick_driver()
        if driver_id is None:
            print("Cancelled.")
            return
    else:
        driver_id = route.driver_id

    # Status
    print(f"Current status: {route.status}")
    if prompt_yes_no("Change status? (y/n): "):
        status = _pick_status()
        if status is None:
            print("Cancelled.")
            return
    else:
        status = route.status

    if update_route(route_id, route_date, driver_id, status):
        print("Route updated.")
    else:
        print("Error: invalid details. No changes made.")


def _delete():
    route_id = prompt_int("Route ID: ")
    if route_id is None:
        return

    route = read_route(route_id)
    if route is None:
        print("Error: route not found.")
        return

    if not prompt_yes_no(
        f"Delete Route #{route.id} ({route.date}, status={route.status})? (y/n): "
    ):
        print("Cancelled.")
        return

    if delete_route(route_id):
        print("Route deleted.")
    else:
        print("Error: could not delete route.")


# ---------------------------------------------------------------------------
# Pickers
# ---------------------------------------------------------------------------
def _prompt_date():
    """Prompt for YYYY-MM-DD. Returns date or None."""
    raw = input("Date (YYYY-MM-DD): ").strip()
    try:
        return date_type.fromisoformat(raw)
    except ValueError:
        print("Error: date must be in YYYY-MM-DD format.")
        return None


def _pick_driver():
    """Show numbered list of drivers; return driver_id, or None."""
    drivers = read_all_delivery_persons()
    if not drivers:
        print("Error: no delivery persons exist. Create one first.")
        return None

    print("\nAvailable drivers:")
    for idx, d in enumerate(drivers, start=1):
        print(f"  {idx}: {d.name}")

    while True:
        raw = input(
            f"Choose driver (1-{len(drivers)}), or 0 to cancel: "
        ).strip()
        try:
            n = int(raw)
        except ValueError:
            print("Error: enter a number.")
            continue
        if n == 0:
            return None
        if 1 <= n <= len(drivers):
            return drivers[n - 1].id
        print(f"Error: enter a number between 1 and {len(drivers)}.")


def _pick_status():
    """Show numbered list of statuses; return selected string, or None."""
    print("\nAvailable statuses:")
    for idx, status in enumerate(ROUTE_STATUSES, start=1):
        print(f"  {idx}: {status}")

    while True:
        raw = input(
            f"Choose status (1-{len(ROUTE_STATUSES)}), or 0 to cancel: "
        ).strip()
        try:
            n = int(raw)
        except ValueError:
            print("Error: enter a number.")
            continue
        if n == 0:
            return None
        if 1 <= n <= len(ROUTE_STATUSES):
            return ROUTE_STATUSES[n - 1]
        print(f"Error: enter a number between 1 and {len(ROUTE_STATUSES)}.")


# ---------------------------------------------------------------------------
# Display helper
# ---------------------------------------------------------------------------
def _print_one(r):
    driver = read_delivery_person(r.driver_id)
    driver_name = driver.name if driver else f"#{r.driver_id}"
    print(
        f"#{r.id} | {r.date} | driver: {driver_name} | status: {r.status}"
    )