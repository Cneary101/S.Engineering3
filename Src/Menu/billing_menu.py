from datetime import date as date_type

from Billing.Billing import (
    read_billing,
    read_all_billings,
    read_billings_by_customer,
    update_billing,
    mark_billing_paid,
    delete_billing,
)
from constants import BILLING_STATUSES
from Customer.Customer import (
    read_all_customers,
    read_customer,
)
from Menu.helpers import (
    prompt_int,
    prompt_yes_no,
)


def billing_menu():
    while True:
        choice = input(
            "\nBilling Menu\n"
            "1: Read (by ID)\n"
            "2: List all\n"
            "3: List by customer\n"
            "4: Mark as paid\n"
            "5: Update\n"
            "6: Delete\n"
            "7: Back\n"
            "Choice: "
        ).strip()

        if choice == "1":
            _read()
        elif choice == "2":
            _list_all()
        elif choice == "3":
            _list_by_customer()
        elif choice == "4":
            _mark_paid()
        elif choice == "5":
            _update()
        elif choice == "6":
            _delete()
        elif choice == "7":
            return
        else:
            print("Error: invalid choice.")


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------
def _read():
    bill_id = prompt_int("Bill ID: ")
    if bill_id is None:
        return

    bill = read_billing(bill_id)
    if bill is None:
        print("Error: bill not found.")
        return
    _print_one(bill)


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------
def _list_all():
    bills = read_all_billings()
    if not bills:
        print("No bills yet.")
        return

    print(f"\n{len(bills)} bill(s):")
    print(f"  {'ID':<5} {'Customer':<25} {'Amount':>8} {'Status':<10} {'Due':<12}")
    print(f"  {'-'*5} {'-'*25} {'-'*8} {'-'*10} {'-'*12}")
    for b in bills:
        _print_summary_row(b)


def _list_by_customer():
    customer_id = _pick_customer()
    if customer_id is None:
        print("Cancelled.")
        return

    customer = read_customer(customer_id)
    bills = read_billings_by_customer(customer_id)
    if not bills:
        print(f"No bills for {customer.name} {customer.last_name}.")
        return

    print(f"\nBills for {customer.name} {customer.last_name}:")
    print(f"  {'ID':<5} {'Amount':>8} {'Status':<10} {'Due':<12}")
    print(f"  {'-'*5} {'-'*8} {'-'*10} {'-'*12}")
    total = 0.0
    unpaid_total = 0.0
    for b in bills:
        print(
            f"  {b.id:<5} {float(b.amount):>8.2f} {b.status:<10} {str(b.due_date):<12}"
        )
        total += float(b.amount)
        if b.status == "unpaid" or b.status == "overdue":
            unpaid_total += float(b.amount)
    print(f"  {'':<5} {'-'*8}")
    print(f"  {'TOTAL':<5} {total:>8.2f}")
    print(f"  {'OUTSTANDING':<5} {unpaid_total:>8.2f} (unpaid + overdue)")


# ---------------------------------------------------------------------------
# Mark paid
# ---------------------------------------------------------------------------
def _mark_paid():
    bill_id = prompt_int("Bill ID: ")
    if bill_id is None:
        return

    bill = read_billing(bill_id)
    if bill is None:
        print("Error: bill not found.")
        return

    if bill.status == "paid":
        print(f"Bill #{bill_id} is already marked as paid.")
        return

    _print_one(bill)
    if not prompt_yes_no(f"Mark bill #{bill_id} as paid? (y/n): "):
        print("Cancelled.")
        return

    if mark_billing_paid(bill_id):
        print(f"Bill #{bill_id} marked as paid.")
    else:
        print("Error: could not mark bill as paid.")


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def _update():
    bill_id = prompt_int("Bill ID: ")
    if bill_id is None:
        return

    bill = read_billing(bill_id)
    if bill is None:
        print("Error: bill not found.")
        return

    _print_one(bill)

    # ----- customer -----
    if prompt_yes_no("Change customer? (y/n): "):
        customer_id = _pick_customer()
        if customer_id is None:
            print("Cancelled.")
            return
    else:
        customer_id = bill.customer_id

    # ----- amount -----
    raw = input(f"Amount [{bill.amount}] (Enter to keep): ").strip()
    if raw == "":
        amount = float(bill.amount)
    else:
        try:
            amount = float(raw)
        except ValueError:
            print("Error: amount must be a number. No changes made.")
            return
        if amount < 0:
            print("Error: amount cannot be negative. No changes made.")
            return

    # ----- status -----
    print(f"Current status: {bill.status}")
    if prompt_yes_no("Change status? (y/n): "):
        status = _pick_status()
        if status is None:
            print("Cancelled.")
            return
    else:
        status = bill.status

    # ----- due date -----
    raw = input(
        f"Due date [{bill.due_date}] (YYYY-MM-DD, Enter to keep): "
    ).strip()
    if raw == "":
        due_date = bill.due_date
    else:
        try:
            due_date = date_type.fromisoformat(raw)
        except ValueError:
            print("Error: date must be YYYY-MM-DD. No changes made.")
            return

    if update_billing(bill_id, customer_id, amount, status, due_date):
        print("Bill updated.")
    else:
        print("Error: invalid details. No changes made.")


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def _delete():
    bill_id = prompt_int("Bill ID: ")
    if bill_id is None:
        return

    bill = read_billing(bill_id)
    if bill is None:
        print("Error: bill not found.")
        return

    _print_one(bill)

    if not prompt_yes_no(
        f"Delete bill #{bill.id} ({bill.amount:.2f}, {bill.status})? (y/n): "
    ):
        print("Cancelled.")
        return

    if delete_billing(bill_id):
        print(f"Bill #{bill_id} deleted.")
    else:
        print("Error: could not delete bill.")


# ---------------------------------------------------------------------------
# Pickers
# ---------------------------------------------------------------------------
def _pick_customer():
    customers = read_all_customers()
    if not customers:
        print("Error: no customers exist.")
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
    print("\nAvailable statuses:")
    for idx, status in enumerate(BILLING_STATUSES, start=1):
        print(f"  {idx}: {status}")

    while True:
        raw = input(
            f"Choose status (1-{len(BILLING_STATUSES)}), or 0 to cancel: "
        ).strip()
        try:
            n = int(raw)
        except ValueError:
            print("Error: enter a number.")
            continue
        if n == 0:
            return None
        if 1 <= n <= len(BILLING_STATUSES):
            return BILLING_STATUSES[n - 1]
        print(f"Error: enter a number between 1 and {len(BILLING_STATUSES)}.")


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------
def _print_one(bill):
    customer = read_customer(bill.customer_id)
    cust_name = (
        f"{customer.name} {customer.last_name}" if customer
        else f"#{bill.customer_id}"
    )
    print(
        f"\nBill #{bill.id}\n"
        f"  Customer: {cust_name}\n"
        f"  Amount:   {float(bill.amount):.2f}\n"
        f"  Status:   {bill.status}\n"
        f"  Due date: {bill.due_date}"
    )


def _print_summary_row(bill):
    customer = read_customer(bill.customer_id)
    cust_name = (
        f"{customer.name} {customer.last_name}" if customer
        else f"#{bill.customer_id}"
    )
    # Truncate long customer names to fit column
    if len(cust_name) > 25:
        cust_name = cust_name[:22] + "..."
    print(
        f"  {bill.id:<5} {cust_name:<25} {float(bill.amount):>8.2f} "
        f"{bill.status:<10} {str(bill.due_date):<12}"
    )