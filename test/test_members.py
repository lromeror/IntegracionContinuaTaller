import pytest
import json
import os
from src.members import register_member, load_data, save_data

DATA_FILE = "data.json"

@pytest.fixture(autouse=True)
def clean_data():
    data = {"members": [], "books": [], "loans": []}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
    yield
    os.remove(DATA_FILE)

def test_register_member_success():
    member = register_member("M001", "Ana Torres")
    assert member["id"] == "M001"
    assert member["name"] == "Ana Torres"

def test_member_saved_to_file():
    register_member("M001", "Ana Torres")
    data = load_data()
    assert any(m["id"] == "M001" for m in data["members"])

def test_register_duplicate_id_raises():
    register_member("M001", "Ana Torres")
    with pytest.raises(ValueError, match="already exists"):
        register_member("M001", "Carlos Pérez")

def test_register_empty_id_raises():
    with pytest.raises(ValueError, match="required"):
        register_member("", "Ana Torres")

def test_register_empty_name_raises():
    with pytest.raises(ValueError, match="required"):
        register_member("M001", "")