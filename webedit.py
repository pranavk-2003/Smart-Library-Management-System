import network
import socket
from time import sleep
import json
import machine
ssid = 'C:\Trojan Horse\Virus.exe'
password = '123456789p'
def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print('Connected on {}'.format(ip))
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def load_data():
    try:
        with open('loans.json', 'r') as f:
            loans = json.load(f)
    except (OSError, ValueError):
        loans = []

    try:
        with open('books.json', 'r') as f:
            books = json.load(f)
    except (OSError, ValueError):
        books = {}

    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except (OSError, ValueError):
        users = {}

    return loans, books, users

def save_data(loans, books, users):
    with open('loans.json', 'w') as f:
        json.dump(loans, f)

    with open('books.json', 'w') as f:
        json.dump(books, f)

    with open('users.json', 'w') as f:
        json.dump(users, f)

def add_user(users, user_name):
    user_id = max(users.keys(), default=0) + 1
    users[user_id] = {'name': user_name, 'books': []}
    return user_id

def add_book(books, book_name, quantity):
    book_id = max(books.keys(), default=0) + 1
    books[book_id] = {'name': book_name, 'quantity': quantity}
    return book_id

def webpage(loans, books, users):
    # Template HTML
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Library Management System</title>
        <style>
            /* ... (CSS styles remain the same) ... */
        </style>
    </head>
    <body>
        <h1>Library Management System</h1>

        <h2>Add User</h2>
        <form method="post" action="/add_user">
            <label for="user_name">User Name:</label>
            <input type="text" id="user_name" name="user_name" required>
            <button type="submit">Add User</button>
        </form>

        <h2>Add Book</h2>
        <form method="post" action="/add_book">
            <label for="book_name">Book Name:</label>
            <input type="text" id="book_name" name="book_name" required>
            <label for="quantity">Quantity:</label>
            <input type="number" id="quantity" name="quantity" min="1" required>
            <button type="submit">Add Book</button>
        </form>

        <h2>Loans</h2>
        <table>
            <tr>
                <th>User ID</th>
                <th>User Name</th>
                <th>Book ID</th>
                <th>Book Name</th>
                <th>Issue Date</th>
                <th>Due Date</th>
            </tr>
            {}
        </table>

        <h2>Books</h2>
        <table>
            <tr>
                <th>Book ID</th>
                <th>Book Name</th>
                <th>Quantity</th>
            </tr>
            {}
        </table>

        <h2>Users</h2>
        <table>
            <tr>
                <th>User ID</th>
                <th>User Name</th>
                <th>Books</th>
            </tr>
            {}
        </table>
    </body>
    </html>
    """.format(
        "".join(["<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            loan['user_id'], loan['user_name'], loan['book_id'], loan['book_name'], loan['issue_date'], loan['due_date']) for loan in loans]),
        "".join(["<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(book_id, book_info['name'], book_info['quantity']) for book_id, book_info in books.items()]),
        "".join(["<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(user_id, user_info['name'], ', '.join([str(book_id) for book_id in user_info['books']])) for user_id, user_info in users.items()])
    )
    return html

def serve(connection):
    # Start a web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)

        loans, books, users = load_data()

        if request.startswith('POST /add_user'):
            user_name = parse_form_data(request)['user_name']
            user_id = add_user(users, user_name)
            save_data(loans, books, users)
            html = f"User '{user_name}' added with ID {user_id}"

        elif request.startswith('POST /add_book'):
            form_data = parse_form_data(request)
            book_name = form_data['book_name']
            quantity = int(form_data['quantity'])
            book_id = add_book(books, book_name, quantity)
            save_data(loans, books, users)
            html = f"Book '{book_name}' added with ID {book_id}"

        else:
            html = webpage(loans, books, users)

        client.sendall(html.encode())
        client.close()

def parse_form_data(request):
    form_data = {}
    lines = request.split('\r\n')
    for line in lines[1:]:
        if line.strip():
            key, value = line.split('=')
            form_data[key] = value
    return form_data

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()