import sqlite3
import Path
from db_connection import get_connection

_connection = get_connection()
cursor = _connection.cursor()

views_folder = Path("views")

for sql_file in views_folder.glob("*.sql"):
    print(f"Creating view from {sql_file.name}...")

    with open(sql_file, 'r', encoding='utf-8') as _file:
        sql_script = _file.read()

    cursor.executescript(sql_script)

_connection.commit()
_connection.close()

print("Finished creating all SQL views.")