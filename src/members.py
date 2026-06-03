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

def register_member(member_id: str, name: str) -> dict:
    if not member_id or not name:
        raise ValueError("ID and name are required.")
    
    data = load_data()
    
    for m in data["members"]:
        if m["id"] == member_id:
            raise ValueError(f"Member with ID '{member_id}' already exists.")
    
    member = {"id": member_id, "name": name}
    data["members"].append(member)
    save_data(data)
    return member