from Login import Login

def main():
    print("Welcome to NewsAgent Delivery systems")
    while True:
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        User = Login(username, password)

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
                         "2: Delivery Person\n"
                         "3: Delivery Docket\n"
                         "4: Orders\n"
                         "5: Exit\n")

        if MainMenu == "1":
            print("Customer")
            while True:
                try:
                    choiceC = input("Please enter your choice:\n"
                                    "1: Create\n"
                                    "2: Read\n"
                                    "3: Update\n"
                                    "4: Delete\n"
                                    "5: Exit\n")
                    if choiceC == "1":
                        print("Create new Customer")
                        pass
                    elif choiceC == "2":
                        print("Read existing Customer")
                        pass
                    elif choiceC == "3":
                        print("Update existing Customer")
                        pass
                    elif choiceC == "4":
                        print("Delete Customer")
                        pass
                    elif choiceC == "5":
                        print("Exiting Customer menu")
                        break
                    else:
                        raise ValueError("Invalid Choice")
                except ValueError as e:
                    print(e)

        elif MainMenu == "2":
            print("Delivery person")
            while True:
                try:
                    choiceD = input("Please enter your choice:\n"
                                    "1: Create\n"
                                    "2: Read\n"
                                    "3: Update\n"
                                    "4: Delete\n"
                                    "5: Exit\n")
                    if choiceD == "1":
                        print("Create new Delivery person")
                        pass
                    elif choiceD == "2":
                        print("Read existing Delivery person")
                        pass
                    elif choiceD == "3":
                        print("Update existing Delivery person")
                        pass
                    elif choiceD == "4":
                        print("Delete Delivery person")
                        pass
                    elif choiceD == "5":
                        print("Exiting Delivery person menu")
                        break
                    else:
                        raise ValueError("Invalid Choice")
                except ValueError as e:
                    print(e)

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