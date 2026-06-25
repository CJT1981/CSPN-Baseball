import sqlite3

# Creating a clean and reusable connection to the database

def get_connection():
    connection = sqlite3.connect('database/baseball.db')
    return connection