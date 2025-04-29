import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'components.db')

def create_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create components table
    c.execute('''
    CREATE TABLE IF NOT EXISTS components (
        id INTEGER PRIMARY KEY, 
        name TEXT, 
        camera_job_tray1 INTEGER DEFAULT 0,
        camera_job_tray2 INTEGER DEFAULT 0,
        camera_job_tray3 INTEGER DEFAULT 0,
        camera_count_job_tray1 INTEGER DEFAULT 0,
        camera_count_job_tray2 INTEGER DEFAULT 0,
        camera_count_job_tray3 INTEGER DEFAULT 0,
        shark_fin INTEGER DEFAULT 0
    )
    ''')


    # Create assemblies table
    c.execute('''
    CREATE TABLE IF NOT EXISTS assemblies (
        id INTEGER PRIMARY KEY,
        name TEXT,
        tray_1 TEXT DEFAULT '',
        tray_2 TEXT DEFAULT '',
        tray_3 TEXT DEFAULT ''
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
