import pytest
import json
import os
from src.members import list_member_loans, save_data

DATA_FILE = "data.json"

@pytest.fixture(autouse=True)
def clean_data():
    data = {"members": [], "books": [], "loans": []}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
    yield
    os.remove(DATA_FILE)

def test_member_with_no_loans_returns_empty():
    save_data({"members": [{"id": "M001", "name": "Ana Torres"}], "books": [], "loans": []})
    assert list_member_loans("M001") == []

def test_member_with_one_loan_returns_book():
    save_data({
        "members": [{"id": "M001", "name": "Ana Torres"}],
        "books": [{"id": "B001", "title": "Clean Code"}],
        "loans": [{"member_id": "M001", "book_id": "B001"}],
    })
    result = list_member_loans("M001")
    assert len(result) == 1
    assert result[0]["id"] == "B001"

def test_member_with_multiple_loans_returns_all_books():
    save_data({
        "members": [{"id": "M001", "name": "Ana Torres"}],
        "books": [
            {"id": "B001", "title": "Clean Code"},
            {"id": "B002", "title": "The Pragmatic Programmer"},
        ],
        "loans": [
            {"member_id": "M001", "book_id": "B001"},
            {"member_id": "M001", "book_id": "B002"},
        ],
    })
    result = list_member_loans("M001")
    ids = [b["id"] for b in result]
    assert "B001" in ids
    assert "B002" in ids

def test_only_returns_loans_for_requested_member():
    save_data({
        "members": [
            {"id": "M001", "name": "Ana Torres"},
            {"id": "M002", "name": "Carlos Pérez"},
        ],
        "books": [
            {"id": "B001", "title": "Clean Code"},
            {"id": "B002", "title": "The Pragmatic Programmer"},
        ],
        "loans": [
            {"member_id": "M001", "book_id": "B001"},
            {"member_id": "M002", "book_id": "B002"},
        ],
    })
    result = list_member_loans("M001")
    assert len(result) == 1
    assert result[0]["id"] == "B001"

def test_nonexistent_member_raises():
    with pytest.raises(ValueError, match="does not exist"):
        list_member_loans("M999")

def test_empty_member_id_raises():
    with pytest.raises(ValueError, match="required"):
        list_member_loans("")
