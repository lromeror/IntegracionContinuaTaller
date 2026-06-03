import json
import os

DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"members": [], "books": [], "loans": []}

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def loan_book(member_id: str, book_id: str) -> dict:
    if not member_id or not book_id:
        raise ValueError("Member ID and book ID are required.")

    data = load_data()

    member_exists = any(member["id"] == member_id for member in data["members"])
    if not member_exists:
        raise ValueError(f"Member with ID '{member_id}' does not exist.")

    book_exists = any(book["id"] == book_id for book in data["books"])
    if not book_exists:
        raise ValueError(f"Book with ID '{book_id}' does not exist.")

    book_already_loaned = any(loan["book_id"] == book_id for loan in data["loans"])
    if book_already_loaned:
        raise ValueError(f"Book with ID '{book_id}' is already on loan.")

    loan = {
        "member_id": member_id,
        "book_id": book_id
    }

    data["loans"].append(loan)
    save_data(data)

    return loan