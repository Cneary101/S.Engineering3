from Login import LoginManager
from Menu import customer_menu, publication_menu

def main():
    print("Welcome to NewsAgent Delivery systems")
    while True:
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        User = LoginManager(username, password)

        if not(User.verifyUsername()):
            print("Invalid Username")
        elif not(User.verifyPassword()):
            print("Invalid Password")
        else:
            break

    print("Welcome! " + username)
    while True:
        MainMenu = input("Please enter your choice:\n"
                         "1: Customer\n"
                         "2: Publication\n"
                         "3: Delivery Docket\n"
                         "4: Orders\n"
                         "5: Exit\n")

        if MainMenu == "1":
            customer_menu()

        elif MainMenu == "2":
           publication_menu()

        elif MainMenu == "3":
            print("Delivery Docket")
            while True:
                try:
                    choiceDD = input("Please enter your choice:\n"
                                     "1: Create\n"
                                     "2: Read\n"
                                     "3: Update\n"
                                     "4: Delete\n"
                                     "5: Exit\n")
                    if choiceDD == "1":
                        print("Create new Delivery Docket")
                        pass
                    elif choiceDD == "2":
                        print("Read existing Delivery Docket")
                        pass
                    elif choiceDD == "3":
                        print("Update existing Delivery Docket")
                        pass
                    elif choiceDD == "4":
                        print("Delete Delivery Docket")
                        pass
                    elif choiceDD == "5":
                        print("Exiting Delivery Docket menu")
                        break
                    else:
                        raise ValueError("Invalid Choice")
                except ValueError as e:
                    print(e)

        elif MainMenu == "4":
            print("Orders")
            while True:
                try:
                    choiceO = input("Please enter your choice:\n"
                                    "1: Create\n"
                                    "2: Read\n"
                                    "3: Update\n"
                                    "4: Delete\n"
                                    "5: Exit\n")
                    if choiceO == "1":
                        print("Create new Order")
                        pass
                    elif choiceO == "2":
                        print("Read existing Order")
                        pass
                    elif choiceO == "3":
                        print("Update existing Order")
                        pass
                    elif choiceO == "4":
                        print("Delete Order")
                        pass
                    elif choiceO == "5":
                        print("Exiting Orders menu")
                        break
                    else:
                        raise ValueError("Invalid Choice")
                except ValueError as e:
                    print(e)
        elif MainMenu == "5":
            print("Goodbye! " + username)
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()