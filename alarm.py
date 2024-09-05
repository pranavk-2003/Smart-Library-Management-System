import json
import time
from mfrc522 import MFRC522
import utime
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd

# Define dictionaries to store records
users = {
    4133544035: {"name": "Alice", "books": []},
    76801299: {"name": "Bob", "books": []}
}

books = {
    3178955690: {"name": "Book 2", "quantity": 3},
    3178573514: {"name": "Book 1", "quantity": 4}
}

# Load data from files or initialize empty data
try:
    with open('loans.json', 'r') as f:
        loans = json.load(f)
except (OSError, ValueError):
    loans = []
# LCD constants
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C and LCD
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# GPIO pin for buzzer
buzzer_pin = Pin(16, Pin.OUT)
buzzer_pin.value(0)  # Set buzzer initially to off

# Function to scan RFID cards
def scan_card(reader):
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            return int.from_bytes(bytes(uid), "little", False)
    return None

# Function to display current date and due date alternately
def display_dates(issue_date, due_date):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Today:{:02d}/{:02d}/{:04d}".format(issue_date[2], issue_date[1], issue_date[0]))
    lcd.move_to(0, 1)
    lcd.putstr("Due:  {:02d}/{:02d}/{:04d}".format(due_date[2], due_date[1], due_date[0]))
    utime.sleep(5)

# Function to display "Thank you" message
def display_thank_you():
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Thank you!")
    lcd.move_to(0, 1)
    lcd.putstr("See you soon!")
    utime.sleep(8)

# Function to lend a book to a user
def lend_book(user_id, book_id):
    issue_date = utime.localtime()
    due_date = utime.localtime(utime.mktime(issue_date) + (15 * 24 * 60 * 60))
    if book_id in books and books[book_id]["quantity"] > 0:
        user_name = users[user_id]["name"]
        book_name = books[book_id]["name"]
        loans.append({"user_id": user_id, "user_name": user_name, "book_id": book_id, "book_name": book_name, "issue_date": str(issue_date), "due_date": str(due_date)})
        users[user_id]["books"].append(book_id)
        books[book_id]["quantity"] -= 1
        with open('books.json', 'w') as f:
            json.dump(books, f)
        with open('loans.json', 'w') as f:
            json.dump(loans, f)
        with open('users.json', 'w') as f:
            json.dump(users, f)
        display_dates(issue_date, due_date)
        return True
    else:
        print("Sorry, this book is currently unavailable.")
    return False

# Function to format time
def format_time(timestamp):
    year, month, day, hour, minute, second, *_ = timestamp
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(year, month, day, hour, minute, second)

# Function to print data in a tabular format
def print_data():
    print("\nLoans:")
    print("+------------+------------+------------+----------------------+----------------------+----------------------+----------+----------+")
    print("| User ID    | User Name  | Book ID    | Book Name            | Issue Date           | Due Date             | Available | Loaned   |")
    print("+------------+------------+------------+----------------------+----------------------+----------------------+----------+----------+")
    for loan in loans:
        issue_date = eval(loan['issue_date'])
        due_date = eval(loan['due_date'])
        issue_date_str = format_time(issue_date)
        due_date_str = format_time(due_date)
        book_id = loan['book_id']
        book_info = books.get(book_id)
        available_quantity = book_info['quantity'] if book_info else 0
        loaned_quantity = sum(1 for l in loans if l['book_id'] == book_id)
        print(f"| {loan['user_id']:>10} | {loan['user_name']:<10} | {book_id:>10} | {loan['book_name']:<20} | {issue_date_str:<20} | {due_date_str:<20} | {available_quantity:>8} | {loaned_quantity:>8} |")
    print("+------------+------------+------------+----------------------+----------------------+----------------------+----------+----------+")

# Buzzer alarm function for potential book theft
def alarm_beep(duration=1):
    start_time = time.time()
    while time.time() - start_time < duration:
        buzzer_pin.value(1)
        utime.sleep_ms(50)
        buzzer_pin.value(0)
        utime.sleep_ms(50)

# Main loop
while True:
    # RFID scanning for user card
    reader = MFRC522(spi_id=0, sck=Pin(6), miso=Pin(4), mosi=Pin(7), cs=Pin(5), rst=Pin(22))
    card = scan_card(reader)
    if card is not None:
        if card in users:
            user_id = card
            user_name = users[user_id]["name"]
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Welcome, " + user_name)  # Display user's name
            lcd.move_to(0, 1)
            lcd.putstr("Scan the book")

            # Start the book scanning loop
            book_scanned = False
            while not book_scanned:
                book_id = scan_card(reader)
                if book_id is not None:
                    if lend_book(user_id, book_id):
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Book allotted to:")
                        lcd.move_to(0, 1)
                        lcd.putstr(user_name + ": " + books[book_id]["name"][:16])  # Truncate book name to 16 characters
                        utime.sleep(5)  # Display the information for 5 seconds
                        display_thank_you()  # Display "Thank you" message
                        print_data()  # Print data in a tabular format
                        book_scanned = True
        else:
            # Handling the case where a book is scanned before the user tag
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Wrong Allotment")
            lcd.move_to(0, 1)
            lcd.putstr("Scan the User ID")
            while True:  # Loop until a user scans a user tag
                card = scan_card(reader)
                alarm_beep()
                if card is not None and card in users:
                    break  # Exit the loop if a valid user tag is scanned

            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Welcome, " + users[card]["name"])  # Display user's name
            lcd.move_to(0, 1)
            lcd.putstr("Scan the book")
            # Continue with book scanning process...
            
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Smart Library" if utime.time() % 2 == 0 else "Scan your card")
    utime.sleep(1)

