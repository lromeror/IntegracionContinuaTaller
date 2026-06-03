import pytest
import json
import os
from src.loans import loan_book, load_data

DATA_FILE = "data.json"


@pytest.fixture(autouse=True)
def clean_data():
    data = {
        "members": [
            {"id": "M001", "name": "Ana Torres"}
        ],
        "books": [
            {"id": "B001", "title": "Clean Code"}
        ],
        "loans": []
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

    yield

    os.remove(DATA_FILE)


def test_loan_book_success():
    loan = loan_book("M001", "B001")

    assert loan["member_id"] == "M001"
    assert loan["book_id"] == "B001"


def test_loan_saved_to_file():
    loan_book("M001", "B001")

    data = load_data()

    assert any(
        loan["member_id"] == "M001" and loan["book_id"] == "B001"
        for loan in data["loans"]
    )


def test_book_already_on_loan_raises():
    loan_book("M001", "B001")

    with pytest.raises(ValueError, match="already on loan"):
        loan_book("M001", "B001")


def test_loan_empty_member_id_raises():
    with pytest.raises(ValueError, match="required"):
        loan_book("", "B001")


def test_loan_empty_book_id_raises():
    with pytest.raises(ValueError, match="required"):
        loan_book("M001", "")


def test_loan_non_existing_member_raises():
    with pytest.raises(ValueError, match="does not exist"):
        loan_book("M999", "B001")


def test_loan_non_existing_book_raises():
    with pytest.raises(ValueError, match="does not exist"):
        loan_book("M001", "B999")