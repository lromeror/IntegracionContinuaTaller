import json
import os
from datetime import datetime

# Default database filename
DB_FILE = "../data.json"

def load_data(filename=DB_FILE):
    """Loads the library data from a JSON file."""
    if not os.path.exists(filename):
        return {"books": {}, "members": {}, "loans": []}
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {filename} is corrupted. Starting with empty data.")
        return {"books": {}, "members": {}, "loans": []}

def get_overdue_loans(data, evaluation_date=None):
    """
    Filters and returns loans that are past their due date.
    evaluation_date defaults to today if not provided (Format: YYYY-MM-DD).
    """
    if evaluation_date is None:
        eval_dt = datetime.today()
    else:
        eval_dt = datetime.strptime(evaluation_date, "%Y-%m-%d")

    overdue_loans = []
    
    for loan in data.get("loans", []):
        # Parse the due date from the loan record
        try:
            due_dt = datetime.strptime(loan["due_date"], "%Y-%m-%d")
        except (ValueError, KeyError):
            # Skip or handle malformed loan records gracefully
            continue
            
        if due_dt < eval_dt:
            # Enrich the loan data with names/titles for a better CLI report
            book_title = data.get("books", {}).get(loan["book_id"], {}).get("title", "Unknown Book")
            member_name = data.get("members", {}).get(loan["member_id"], {}).get("name", "Unknown Member")
            
            overdue_loans.append({
                "book_id": loan["book_id"],
                "book_title": book_title,
                "member_id": loan["member_id"],
                "member_name": member_name,
                "due_date": loan["due_date"],
                "days_overdue": (eval_dt - due_dt).days
            })
            
    return overdue_loans

def report_overdue_loans(filename=DB_FILE):
    """Fetches and prints the overdue loans in a clean CLI format."""
    data = load_data(filename)
    # Using current date for real-world CLI execution
    overdue = get_overdue_loans(data)
    
    print("\n=== OVERDUE LOANS REPORT ===")
    if not overdue:
        print("No overdue loans found! Everything is up to date.")
        return

    print(f"{'Member':<20} | {'Book Title':<30} | {'Due Date':<12} | {'Days Overdue'}")
    print("-" * 75)
    for loan in overdue:
        print(f"{loan['member_name']:<20} | {loan['book_title']:<30} | {loan['due_date']:<12} | {loan['days_overdue']} days")
    print(f"Total Overdue Items: {len(overdue)}\n")

if __name__ == "__main__":
    # This allows you to quickly test the report via command line directly
    report_overdue_loans()