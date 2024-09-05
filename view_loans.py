import json

# Load data from files
with open('loans.json', 'r') as f:
    loans = json.load(f)

# Print the loans data
print("Loans:")
print("+------------+------------+------------+----------------------+----------------------+")
print("| User ID    | User Name  | Book ID    | Book Name            | Due Date             |")
print("+------------+------------+------------+----------------------+----------------------+")
for loan in loans:
    print(f"| {loan['user_id']:>10} | {loan['user_name']:<10} | {loan['book_id']:>10} | {loan['book_name']:<20} | {loan['due_date']:>20} |")
print("+------------+------------+------------+----------------------+----------------------+")
