
from datetime import date


def prompt_int(prompt):
    """Prompt once for a whole number. Returns int or None on bad input."""
    try:
        return int(input(prompt))
    except ValueError:
        print("Error: enter a whole number.")
        return None


def prompt_required_int(prompt):
    """Loop until a whole number is entered. Never returns None."""
    while True:
        value = prompt_int(prompt)
        if value is not None:
            return value


def prompt_text(prompt, allow_empty=False):
    """Prompt for text; loop if empty and not allowed."""
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("Error: field cannot be empty.")


def prompt_phone(prompt, current=None, allow_blank_for_keep=False):
    """Phone must be exactly 10 digits (matches crud.customer.verify_phone_number)."""
    while True:
        hint = f" [{current}]" if current else ""
        raw = input(f"{prompt}{hint}: ").strip()
        if allow_blank_for_keep and raw == "":
            return current
        if len(raw) == 10 and raw.isdigit():
            return raw
        print("Error: phone must be exactly 10 digits (no dashes or spaces).")


def prompt_yes_no(prompt):
    """Returns True for y/yes, False for n/no, re-prompts otherwise."""
    while True:
        value = input(prompt).strip().lower()
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("Error: answer 'y' or 'n'.")


def prompt_date(prompt):
    """Prompt for a date in YYYY-MM-DD. Returns a date object or None."""
    raw = input(f"{prompt} (YYYY-MM-DD): ").strip()
    try:
        return date.fromisoformat(raw)
    except ValueError:
        print("Error: date must be in YYYY-MM-DD format.")
        return None