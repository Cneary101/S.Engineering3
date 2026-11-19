from getpass import getpass

from sqlalchemy.orm import Session

from database import engine
from Login import LoginManager
from Menu import customer_menu, publication_menu, delivery_person_menu, docket_menu, order_menu, billing_menu, newsagent_menu


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
                    "7: Newsagents\n"
                    "8: Exit\n"
                    "Choice: "
                ).strip()
            if choice == "1":
                customer_menu()

            elif choice == "2":
                publication_menu()

            elif choice == "3":
                delivery_person_menu()

            elif choice == "4":
                docket_menu()

            elif choice == "5":
                order_menu()

            elif choice == "6":
                billing_menu()

            elif choice == "7":
                newsagent_menu()

            elif choice == "8":
                print(f"Goodbye, {user.username}!")
                break

            else:
                print("Invalid choice.")


if __name__ == "__main__":
    main()
