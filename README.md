---

# Smart Library Management System

## Overview

The **Smart Library Management System** is an IoT-based project designed to efficiently manage a library's book lending process. It incorporates features such as tracking book loans, managing user data, and displaying information on an LCD screen. The project also includes a web interface for easier interaction with the system.

## Features

- **Book and User Management:** Store information about books and users in JSON format.
- **Loan Management:** Track the status of loans and available books.
- **LCD Display:** Show relevant information using an I2C LCD screen.
- **Web Interface:** View and edit book loans and user data through a web-based interface.
- **RFID Integration:** Likely includes support for RFID using the MFRC522 module to manage book checkouts and returns.

## Project Structure

- **Python Files:**
  - `main.py`: The central script that runs the core system functionality.
  - `db.py`: Handles database operations related to books, users, and loans.
  - `mfrc522.py`: Module for RFID card reader (MFRC522) interaction.
  - `pico_i2c_lcd.py`: Functions for controlling the I2C LCD display.
  - `view_loans.py`, `webedit.py`, `webview.py`, `website.py`: Web interface functionalities for viewing and editing data.
  - `lcd_api.py`, `lcd_eg.py`: Code for interacting with the LCD screen.
  - `data_read.py`, `read_loans.py`: Scripts for reading data from JSON files.
  - `clear_data.py`: Script for clearing or resetting the stored data.

- **HTML File:**
  - `index.html`: The main webpage interface for the system.

- **JSON Files:**
  - `books.json`: Stores book information (title, author, availability).
  - `users.json`: Stores user information (ID, name, contact details).
  - `loans.json`: Keeps track of the book loans (user ID, book ID, due dates).

## Requirements

To run this project, you will need:

- Python 3.x
- `Flask` (or any other Python web framework for handling the web interface)
- I2C LCD display
- RFID module (MFRC522)
  
## Setup

1. Clone the repository from GitHub:
   ```bash
   git clone https://github.com/your-username/smart-library-management-system.git
   cd smart-library-management-system
   ```

2. Install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the main system:
   ```bash
   python main.py
   ```

4. Access the web interface by navigating to `localhost:5000` in your browser.

## Usage

- **Web Interface:** Manage book loans, view user details, and edit records through the web interface.
- **LCD Display:** Displays important messages and updates regarding book checkouts and returns.
- **RFID:** Use the RFID reader for quick book loans and returns.

## Future Enhancements

- Integrate with a more advanced database system (e.g., SQLite or MySQL) for scalability.
- Implement user authentication for the web interface.
- Add more robust error handling and logging.

---
