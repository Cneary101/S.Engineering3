"Separate menus for the Publication, Newsagent and Billing classes."

from datetime import date
from Publication_Basic import PublicationManager
from Newsagent_Basic import NewsagentManager
from billing import BillManager


# Convert terminal input to numbers, or show an error.
def whole_number(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Error: Enter a whole number.")
        return None


def price_number(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print("Error: Enter a number.")
        return None


def publication_menu(manager):
    while True:
        choice = input("\nPublication Menu\n" 
        "1: Create\n" 
        "2: Read\n" 
        "3: Update\n" 
        "4: Delete (deactivate)\n" 
        "5: Back\n" 
        "Choice: ")

        if choice == "1":
            publication_id = whole_number("Publication ID: ")
            if publication_id is None:
                continue
            name = input("Name: ")
            publication_type = input("Type: ")
            price = price_number("Price: ")
            quantity = whole_number("Quantity: ")
            frequency = input("Frequency: ")
            if price is None or quantity is None:
                continue

            result = manager.create_publication(publication_id, name, publication_type,
                                                price, quantity, frequency)
            if result is not False:
                print("Publication created successfully.")
            else:
                print("Error: Invalid details or duplicate publication ID.")

        elif choice == "2":
            publication_id = whole_number("Publication ID: ")
            publication = manager.read_publication(publication_id)
            if publication is None:
                print("Error: Publication not found.")
            else:
                print(f"ID: {publication.getPublicationId()}, Name: {publication.getName()}, "
                      f"Type: {publication.getPublicationType()}, Price: {publication.getPrice():.2f}, "
                      f"Quantity: {publication.getQuantity()}, Frequency: {publication.getFrequency()}, "
                      f"Active: {publication.getActive()}")
                if publication.verifyLowStock():
                    print("Warning: Low stock (5 or fewer copies).")

        elif choice == "3":
            publication_id = whole_number("Publication ID: ")
            publication = manager.read_publication(publication_id)
            if publication is None:
                print("Error: Publication not found.")
                continue

            name = publication.getName()
            publication_type = publication.getPublicationType()
            price = publication.getPrice()
            quantity = publication.getQuantity()
            frequency = publication.getFrequency()

            field = input("Change 1: Name, 2: Price, 3: Quantity, 4: Type, 5: Frequency: ")
            if field == "1":
                name = input("New name: ")
            elif field == "2":
                price = price_number("New price: ")
            elif field == "3":
                quantity = whole_number("New quantity: ")
            elif field == "4":
                publication_type = input("New type: ")
            elif field == "5":
                frequency = input("New frequency: ")
            else:
                print("Error: Invalid choice.")
                continue

            if manager.update_publication(publication_id, name, publication_type,
                                          price, quantity, frequency):
                print("Publication updated.")
            else:
                print("Error: Invalid publication details. No changes were made.")

        elif choice == "4":
            publication_id = whole_number("Publication ID: ")
            publication = manager.read_publication(publication_id)
            if publication is None:
                print("Error: Publication not found.")
            elif manager.delete_publication(publication_id):
                print("Publication deactivated.")
            else:
                print("Error: Publication is already inactive.")

        elif choice == "5":
            return
        else:
            print("Error: Invalid choice.")


def newsagent_menu(manager):
    while True:
        choice = input("\nNewsagent Menu\n"
        "1: Create\n" 
        "2: Read\n" 
        "3: Update\n" 
        "4: Delete (deactivate)\n" 
        "5: Back\n" 
        "Choice: ")

        if choice == "1":
            newsagent_id = whole_number("Newsagent ID: ")
            if newsagent_id is None:
                continue
            name = input("Name: ")
            if manager.create_newsagent(newsagent_id, name) is not False:
                print("Newsagent created successfully.")
            else:
                print("Error: Invalid details or duplicate newsagent ID.")

        elif choice == "2":
            newsagent_id = whole_number("Newsagent ID: ")
            newsagent = manager.read_newsagent(newsagent_id)
            if newsagent is None:
                print("Error: Newsagent not found.")
            else:
                print(f"ID: {newsagent.getNewsagentId()}, Name: {newsagent.getName()}, "
                      f"Active: {newsagent.getActive()}")
                
        elif choice == "3":
            newsagent_id = whole_number("Newsagent ID: ")
            name = input("New name: ")
            if manager.update_newsagent(newsagent_id, name):
                print("Newsagent updated.")
            else:
                print("Error: Invalid name or newsagent ID.")

        elif choice == "4":
            newsagent_id = whole_number("Newsagent ID: ")
            newsagent = manager.read_newsagent(newsagent_id)
            if newsagent is None:
                print("Error: Newsagent not found.")
            elif manager.delete_newsagent(newsagent_id):
                print("Newsagent deactivated.")
            else:
                print("Error: Newsagent is already inactive.")

        elif choice == "5":
            return
        else:
            print("Error: Invalid choice.")


def billing_menu(manager, deliveries):
    while True:
        choice = input("\nBilling Menu" 
        "\n1: Record delivery" 
        "\n2: Create bill" 
        "\n3: Read bill" 
        "\n4: Update bill" 
        "\n5: Delete bill" 
        "\n6: Back" 
        "\nChoice: ")

        if choice == "1":
            customer_id = whole_number("Customer ID: ")
            delivery_date = input("Delivery date (YYYY-MM-DD): ")
            price = price_number("Unit price: ")
            quantity = whole_number("Quantity: ")
            delivered = input("Delivered? (y/n): ").strip().lower()
            try:
                date.fromisoformat(delivery_date)
                valid_date = True
            except ValueError:
                valid_date = False
            if (customer_id is None or customer_id <= 0 or not valid_date or
                    price is None or price < 0 or quantity is None or quantity <= 0 or
                    delivered not in ("y", "n")):
                print("Error: Invalid delivery details. Nothing was recorded.")
                continue

            deliveries.append({"customer_id": customer_id, "date": delivery_date,
                               "price": price, "quantity": quantity,
                               "delivered": delivered == "y"})
            print("Delivery recorded for billing.")

        elif choice == "2":
            bill_id = whole_number("Bill ID: ")
            customer_id = whole_number("Customer ID: ")
            month = input("Billing month (YYYY-MM): ")
            if manager.create_bill(bill_id, customer_id, month, deliveries) is not False:
                bill = manager.read_bill(bill_id)
                print(f"Bill created. Total: {bill.getTotal():.2f}")
            else:
                print("Error: Invalid details or duplicate bill ID.")

        elif choice == "3":
            bill_id = whole_number("Bill ID: ")
            bill = manager.read_bill(bill_id)
            if bill is None:
                print("Error: Bill not found.")
            else:
                print(f"Bill ID: {bill.getBillId()}, Customer ID: {bill.getCustomerId()}, "
                      f"Month: {bill.getMonth()}, Total: {bill.getTotal():.2f}")

        elif choice == "4":
            bill_id = whole_number("Bill ID: ")
            customer_id = whole_number("Customer ID: ")
            month = input("Billing month (YYYY-MM): ")
            if manager.update_bill(bill_id, customer_id, month, deliveries):
                print("Bill updated.")
            else:
                print("Error: Invalid details or bill ID.")

        elif choice == "5":
            bill_id = whole_number("Bill ID: ")
            if manager.delete_bill(bill_id):
                print("Draft bill deleted.")
            else:
                print("Error: Bill not found.")

        elif choice == "6":
            return
        else:
            print("Error: Invalid choice.")