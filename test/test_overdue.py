import sys
import os

# Find the path to the parent directory and add it to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.overdue_tracker import get_overdue_loans

class TestOverdueLoans(unittest.TestCase):

    def setUp(self):
        """Set up dummy library state data for testing."""
        self.sample_data = {
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
        # Explicit evaluation date for deterministic test results
        self.eval_date = "2026-06-03"

    def test_overdue_loans_detection(self):
        """Test that only loans strictly before the evaluation date are caught."""
        overdue = get_overdue_loans(self.sample_data, evaluation_date=self.eval_date)
        
        # We expect exactly 2 books to be overdue (The Hobbit and Dune)
        self.assertEqual(len(overdue), 2)
        
        # Check specific details of the first expected overdue book (The Hobbit)
        hobbit_loan = next(l for l in overdue if l["book_id"] == "B001")
        self.assertEqual(hobbit_loan["member_name"], "Alice Smith")
        self.assertEqual(hobbit_loan["book_title"], "The Hobbit")
        # 2026-06-03 minus 2026-05-15 = 19 days
        self.assertEqual(hobbit_loan["days_overdue"], 19)

    def test_no_overdue_loans(self):
        """Test that if the evaluation date is early enough, nothing is flagged."""
        early_eval_date = "2026-05-01"
        overdue = get_overdue_loans(self.sample_data, evaluation_date=early_eval_date)
        
        self.assertEqual(len(overdue), 0)

if __name__ == "__main__":
    unittest.main()