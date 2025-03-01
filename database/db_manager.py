import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'components.db')

def get_all_components():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM components")
    components = c.fetchall()
    conn.close()
    return components

def add_component(name, camera_job):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO components (name, camera_job) VALUES (?, ?)", (name, camera_job))
    conn.commit()
    conn.close()

def add_assembly(name, components):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO assemblies (name, components) VALUES (?, ?)", (name, ','.join(components)))
    conn.commit()
    conn.close()