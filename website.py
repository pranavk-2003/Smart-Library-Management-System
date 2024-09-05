import network
import socket
from time import sleep
import json

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

def webpage(loans, books, users):
    # Template HTML
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Library Management System</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                color: #333;
                margin: 0;
                padding: 20px;
            }}

            h1 {{
                text-align: center;
                color: #004080;
            }}

            h2 {{
                color: #004080;
                margin-top: 30px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th, td {{
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}

            th {{
                background-color: #004080;
                color: #fff;
            }}

            tr:hover {{
                background-color: #f5f5f5;
            }}
        </style>
    </head>
    <body>
        <h1>Library Management System</h1>

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
        html = webpage(loans, books, users)
        client.sendall(html.encode())
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    pass