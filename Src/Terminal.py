from getpass import getpass

from sqlalchemy.orm import Session

from database import engine
from Login import LoginManager
from Menu import customer_menu, publication_menu


def login_flow(session):
    """Prompt for credentials until LoginManager accepts them. Returns the User row."""
    print("Welcome to NewsAgent Delivery systems")
    lm = LoginManager(session)

    while True:
        username = input("Username (6-12 chars): ").strip()
        password = getpass("Password (4-6 digits): ")

        user = lm.authenticate_user(username, password)
        if user is None:
            print("Invalid username or password. Try again.")
        else:
            print(f"Welcome, {user.username}! (role: {user.role})")
            return user


def main():
    with Session(engine) as session:
        user = login_flow(session)

        while True:
            print()
            choice = input(
                "Main Menu\n"
                "1: Customers\n"
                "2: Publications\n"
                "3: Delivery Persons\n"
                "4: Delivery Dockets\n"
                "5: Orders\n"
                "6: Billing\n"
                "7: Exit\n"
                "Choice: "
            ).strip()

            if choice == "1":
                customer_menu()

            elif choice == "2":
                publication_menu()

            elif choice == "3":
                # TODO: uncomment when Menu/delivery_person_menu.py exists
                # delivery_person_menu()
                print("Delivery Persons — not yet implemented.")

            elif choice == "4":
                # TODO: uncomment when Menu/docket_menu.py exists
                # docket_menu()
                print("Delivery Dockets — not yet implemented.")

            elif choice == "5":
                # TODO: uncomment when Menu/order_menu.py exists
                # order_menu()
                print("Orders — not yet implemented.")

            elif choice == "6":
                # TODO: uncomment when Menu/billing_menu.py exists
                # billing_menu()
                print("Billing — not yet implemented.")

            elif choice == "7":
                print(f"Goodbye, {user.username}!")
                break

            else:
                print("Invalid choice.")


if __name__ == "__main__":
    main()