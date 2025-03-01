import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'components.db')

def create_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS components (
                    id INTEGER PRIMARY KEY, 
                    name TEXT, 
                    camera_job BOOLEAN)''')
    c.execute('''CREATE TABLE IF NOT EXISTS assemblies (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    components TEXT)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()