import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'components.db')

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Fetch all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:", tables)

# Fetch all rows from the 'components' table
cursor.execute("SELECT * FROM components")
rows = cursor.fetchall()

cursor.execute("SELECT * FROM assemblies")
assemblies = cursor.fetchall()

print("\nContents of the 'assemblies' table:")
for row in assemblies:
    print(row)


# Display the results
print("\nContents of the 'components' table:")
for row in rows:
    print(row)

# Close the connection
conn.close()
