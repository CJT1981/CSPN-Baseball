import pandas as pd
import sqlite3

# Load my csv data
dframe = pd.read_csv('..\data\y00-26_batting_data.csv')

# Connect to SQLite database
connection = sqlite3.connect('baseball.db')

# Write the DataFrame to a SQL table named 'batting_statistics'
dframe.to_sql(
    'batting_statistics', 
    connection, if_exists='replace', 
    index=False
)

connection.close()

print("Database created successfully and data inserted into 'batting_statistics' table.")
