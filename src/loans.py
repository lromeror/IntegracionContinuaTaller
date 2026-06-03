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
    member_exists = any(m["id"] == member_id for m in data["members"])
    if not member_exists:
        raise ValueError(f"Member with ID '{member_id}' does not exist.")
    book_exists = any(b["id"] == book_id for b in data["books"])
    if not book_exists:
        raise ValueError(f"Book with ID '{book_id}' does not exist.")
    book_already_loaned = any(l["book_id"] == book_id for l in data["loans"])
    if book_already_loaned:
        raise ValueError(f"Book with ID '{book_id}' is already on loan.")
    loan = {"member_id": member_id, "book_id": book_id}
    data["loans"].append(loan)
    save_data(data)
    return loan