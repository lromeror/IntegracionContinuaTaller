import sys
import os

# Find the path to the parent directory and add it to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.overdue_tracker import get_overdue_loans


@pytest.fixture
def library_data():
    """Fixture providing dummy library state data and an evaluation date."""
    sample_data = {
        "books": {
            "B001": {"title": "The Hobbit"},
            "B002": {"title": "1984"},
            "B003": {"title": "Dune"}
        },
        "members": {
            "M001": {"name": "Alice Smith"},
            "M002": {"name": "Bob Jones"}
        },
        "loans": [
            {
                "book_id": "B001",
                "member_id": "M001",
                "due_date": "2026-05-15"  # Overdue if evaluated in June
            },
            {
                "book_id": "B002",
                "member_id": "M002",
                "due_date": "2026-06-10"  # Not overdue if evaluated in June 3rd
            },
            {
                "book_id": "B003",
                "member_id": "M001",
                "due_date": "2026-06-01"  # Overdue if evaluated in June 3rd
            }
        ]
    }
    eval_date = "2026-06-03"
    return sample_data, eval_date


def test_overdue_loans_detection(library_data):
    """Test that only loans strictly before the evaluation date are caught."""
    sample_data, eval_date = library_data
    overdue = get_overdue_loans(sample_data, evaluation_date=eval_date)
    
    # We expect exactly 2 books to be overdue (The Hobbit and Dune)
    assert len(overdue) == 2
    
    # Check specific details of the first expected overdue book (The Hobbit)
    hobbit_loan = next(l for l in overdue if l["book_id"] == "B001")
    assert hobbit_loan["member_name"] == "Alice Smith"
    assert hobbit_loan["book_title"] == "The Hobbit"
    # 2026-06-03 minus 2026-05-15 = 19 days
    assert hobbit_loan["days_overdue"] == 19


def test_no_overdue_loans(library_data):
    """Test that if the evaluation date is early enough, nothing is flagged."""
    sample_data, _ = library_data
    early_eval_date = "2026-05-01"
    overdue = get_overdue_loans(sample_data, evaluation_date=early_eval_date)
    
    assert len(overdue) == 0