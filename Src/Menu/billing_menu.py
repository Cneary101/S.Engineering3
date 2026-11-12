from Billing import (
    create_bill, read_bill, read_all_bills,
    update_bill, update_bill_status, delete_bill,
)
from Menu.helpers import prompt_int, prompt_text, prompt_date, prompt_yes_no


def billing_menu():
    while True:
        choice = input(
            "\nBilling Menu\n"
            "1: Create\n2: Read (by ID)\n3: List all\n"
            "4: Recalculate draft\n5: Issue\n6: Mark paid\n"
            "7: Delete draft\n8: Back\nChoice: "
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
            _issue()
        elif choice == "6":
            _pay()
        elif choice == "7":
            _delete()
        elif choice == "8":
            return
        else:
            print("Error: invalid choice.")


def _create():
    bill_id = prompt_int("Bill ID: ")
    customer_id = prompt_int("Customer ID: ")
    month = prompt_text("Billing month (YYYY-MM): ")
    if bill_id is None or customer_id is None:
        return
    result = create_bill(bill_id, customer_id, month)
    if result is False:
        print("Error: invalid details, unknown customer or duplicate ID.")
    else:
        print(f"Bill #{result} created.")


def _read():
    bill_id = prompt_int("Bill ID: ")
    if bill_id is None:
        return
    bill = read_bill(bill_id)
    if bill is None:
        print("Error: bill not found.")
    else:
        _print_one(bill)


def _list_all():
    bills = read_all_bills()
    if not bills:
        print("No bills yet.")
    for bill in bills:
        _print_one(bill)


def _update():
    bill_id = prompt_int("Bill ID: ")
    if bill_id is None:
        return
    bill = read_bill(bill_id)
    if bill is None:
        print("Error: bill not found.")
        return
    customer_id = prompt_int(f"Customer ID [{bill.customer_id}]: ")
    month = input(f"Month [{bill.month}]: ").strip() or bill.month
    if customer_id is None:
        return
    print("Draft bill updated." if update_bill(bill_id, customer_id, month)
          else "Error: bill must be a draft with valid details.")


def _issue():
    bill_id = prompt_int("Bill ID: ")
    if bill_id is None:
        return
    due_date = prompt_date("Due date")
    if due_date is None:
        return
    print("Bill issued." if update_bill_status(bill_id, "Issued", due_date)
          else "Error: only a draft bill can be issued.")


def _pay():
    bill_id = prompt_int("Bill ID: ")
    if bill_id is None:
        return
    print("Bill marked paid." if update_bill_status(bill_id, "Paid")
          else "Error: only an issued bill can be paid.")


def _delete():
    bill_id = prompt_int("Bill ID: ")
    if bill_id is None:
        return
    bill = read_bill(bill_id)
    if bill is None:
        print("Error: bill not found.")
        return
    if prompt_yes_no(f"Delete draft bill #{bill_id}? (y/n): "):
        print("Draft bill deleted." if delete_bill(bill_id)
              else "Error: only draft bills can be deleted.")
    else:
        print("Cancelled.")


def _print_one(bill):
    due = bill.due_date.isoformat() if bill.due_date else "Not set"
    print(f"#{bill.id} | customer: {bill.customer_id} | month: {bill.month} | "
          f"amount: {bill.amount:.2f} | status: {bill.status} | due: {due}")
