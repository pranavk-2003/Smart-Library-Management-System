import json

# Load data from files
with open('users.json', 'r') as f:
    users = json.load(f)

with open('books.json', 'r') as f:
    books = json.load(f)

# Clear the loans data
loans = []

# Save the updated loans data to a file
with open('loans.json', 'w') as f:
    json.dump(loans, f)

# Print the updated data
print("Users:")
print(users)
print("\nBooks:")
print(books)
print("\nLoans:")
print(loans)
