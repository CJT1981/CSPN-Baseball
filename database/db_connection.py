import sqlite3
from pathlib import Path

# Creating a clean and reusable connection to the database

# App was having problems finding the database since it runs from outside 
# the database folder. This function will create a connection to the database
# from anywhere in the app by using the Path module to find the absolute path to the database file.

base_path = Path(__file__).resolve().parent
database_path = base_path / 'baseball.db'


def get_connection():
    connection = sqlite3.connect(database_path)
    return connection