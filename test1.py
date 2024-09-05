from mfrc522 import MFRC522
import utime
from machine import I2C
from pico_i2c_lcd import I2cLcd

# Define books and their quantities
books = {
    3178955690: {"name": "Book 1", "quantity": 3},
    3178573514: {"name": "Book 2", "quantity": 4},
    76801299: {"name": "Book 3", "quantity": 1}
}

# Define user RFID tag IDs and names
user_tags = {
    4133544035: "Alice",
    76801299: "Bob"
}

# LCD constants
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C and LCD
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

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
def display_dates():
    current_date = utime.localtime()
    due_date = utime.localtime(utime.mktime(current_date) + (15 * 24 * 60 * 60))
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Today:{:02d}/{:02d}/{:04d}".format(current_date[2], current_date[1], current_date[0]))
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

# Main loop
while True:
    # Toggle between "Smart Library" and "Scan your card" on the LCD
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Smart Library" if utime.time() % 2 == 0 else "Scan your card")
    utime.sleep(1)

    # RFID scanning for user card
    reader = MFRC522(spi_id=0, sck=6, miso=4, mosi=7, cs=5, rst=22)
    card = scan_card(reader)
    if card is not None:
        if card in user_tags:
            user_name = user_tags[card]
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Welcome, " + user_name)  # Display user's name
            lcd.move_to(0, 1)
            lcd.putstr("Scan the book")
            utime.sleep(8)  # Delay for better user experience

            # Start the book scanning loop
            while True:
                book_id = scan_card(reader)
                if book_id is not None:
                    if book_id in books:
                        book = books[book_id]
                        if book["quantity"] > 0:
                            lcd.clear()
                            lcd.move_to(0, 0)
                            lcd.putstr("Book allotted to:")
                            lcd.move_to(0, 1)
                            lcd.putstr(user_name + ": " + book["name"][:16])  # Truncate book name to 16 characters
                            book["quantity"] -= 1
                            if book["quantity"] == 0:
                                print("Sorry, this book is currently unavailable.")
                            else:
                                print("Book allotted to " + user_name)
                            utime.sleep(5)  # Display the information for 5 seconds
                            display_dates()  # Display current date and due date alternately
                            display_thank_you()  # Display "Thank you" message
                            break  # Exit the book scanning loop and go back to the main loop
                        else:
                            lcd.clear()
                            lcd.move_to(0, 0)
                            lcd.putstr("Sorry, this book")
                            lcd.move_to(0, 1)
                            lcd.putstr("is unavailable.")
                            utime.sleep(5)  # Delay for better user experience
                    else:
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Unknown book.")
                        lcd.move_to(0, 1)
                        lcd.putstr("Scan another.")
                        utime.sleep(5)  # Delay for better user experience
                else:
                    # No book scanned within a certain time, go back to the main loop
                    break  # Exit the book scanning loop and continue to the main loop
