import sqlite3
from pathlib import Path
from db_connection import get_connection

_connection = get_connection()
cursor = _connection.cursor()

views_folder = Path("views")

for sql_file in views_folder.glob("*.sql"):
    print(f"Creating view from {sql_file.name}...")

    with open(sql_file, 'r', encoding='utf-8') as _file:
        sql_script = _file.read()

    try:
        cursor.executescript(sql_script)
        print(f"{sql_file.name} view created successfully.")

    except sqlite3.Error as e:
        print(f"Error occurred while creating view from {sql_file.name}: {e}")
        break  # Stop processing further if an error occurs

_connection.commit()
_connection.close()

print("Finished creating all SQL views.")