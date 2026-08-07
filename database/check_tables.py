from db_connection import get_connection

connection = get_connection()
cursor = connection.cursor()

"""
    # Check if the tables exist in the database
    cursor.execute("
        SELECT name 
        FROM sqlite_master 
        WHERE type='table';
    ")

    tables = cursor.fetchall()

    print("Tables in the database:")
    for table in tables:
        print(table[0])
"""

cursor.execute("PRAGMA table_info(batting_statistics);")

print("Columns in the 'batting_statistics' table:\n")

columns = cursor.fetchall()
for column in columns:
    print(column[1])  # Print the column name (second element of the tuple)

connection.close()