import json
with open('loans.json', 'r') as f:
    users = json.load(f)
print(users)