import json
import sys
from pathlib import Path

DATA_FILE = Path("data.json")

def load_data():
    if not DATA_FILE.exists():
        return {"books": [], "members": [], "loans": [], "fines": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def return_book(book_code):
    data = load_data()
    loans = data["loans"]

    found = -1
    for i in range(len(loans)):
        if loans[i]["book_code"] == book_code and loans[i]["returned"] == False:
            found = i
            break

    if found == -1:
        print(f"ese libro no está prestado o ya fue devuelto: {book_code}")
        return False

    member_id = loans[found]["member_id"]
    loans[found]["returned"] = True

    for b in data["books"]:
        if b["code"] == book_code:
            b["available"] = True

    save_data(data)
    print(f"listo, {book_code} devuelto por {member_id}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: python return_book.py <codigo>")
        sys.exit(1)

    ok = return_book(sys.argv[1])
    if not ok:
        sys.exit(1)