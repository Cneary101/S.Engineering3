from Newsagent import (
    create_newsagent, read_newsagent, read_all_newsagents,
    update_newsagent, delete_newsagent,
)
from Menu.helpers import prompt_int, prompt_text, prompt_yes_no


def newsagent_menu():
    while True:
        choice = input(
            "\nNewsagent Menu\n"
            "1: Create\n2: Read (by ID)\n3: List all\n"
            "4: Update\n5: Deactivate\n6: Back\nChoice: "
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


def _create():
    newsagent_id = prompt_int("Newsagent ID: ")
    if newsagent_id is None:
        return
    name = prompt_text("Name: ")
    result = create_newsagent(newsagent_id, name)
    print(f"Newsagent #{result} created." if result is not False
          else "Error: invalid details or duplicate ID.")


def _read():
    newsagent_id = prompt_int("Newsagent ID: ")
    if newsagent_id is None:
        return
    newsagent = read_newsagent(newsagent_id)
    if newsagent is None:
        print("Error: newsagent not found.")
    else:
        _print_one(newsagent)


def _list_all():
    newsagents = read_all_newsagents()
    if not newsagents:
        print("No newsagents yet.")
    for newsagent in newsagents:
        _print_one(newsagent)


def _update():
    newsagent_id = prompt_int("Newsagent ID: ")
    if newsagent_id is None:
        return
    newsagent = read_newsagent(newsagent_id)
    if newsagent is None:
        print("Error: newsagent not found.")
        return
    name = input(f"Name [{newsagent.name}]: ").strip() or newsagent.name
    print("Newsagent updated." if update_newsagent(newsagent_id, name)
          else "Error: invalid name.")


def _delete():
    newsagent_id = prompt_int("Newsagent ID: ")
    if newsagent_id is None:
        return
    newsagent = read_newsagent(newsagent_id)
    if newsagent is None:
        print("Error: newsagent not found.")
        return
    if not newsagent.is_active:
        print("Error: newsagent already inactive.")
        return
    if prompt_yes_no(f"Deactivate {newsagent.name}? (y/n): "):
        print("Newsagent deactivated." if delete_newsagent(newsagent_id)
              else "Error: unable to deactivate newsagent.")
    else:
        print("Cancelled.")


def _print_one(newsagent):
    print(f"#{newsagent.id} | {newsagent.name} | active: {newsagent.is_active}")
