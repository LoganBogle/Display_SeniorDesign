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

def add_component(name, tray1, tray2, tray3):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO components (name, camera_job_1, camera_job_2, camera_job_3) VALUES (?, ?, ?, ?)", 
              (name, tray1, tray2, tray3))
    conn.commit()
    conn.close()


def add_assembly(name, tray1, tray2, tray3):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO assemblies (name, tray_1, tray_2, tray_3) VALUES (?, ?, ?, ?)", 
              (name, ','.join(tray1), ','.join(tray2), ','.join(tray3)))
    conn.commit()
    conn.close()

def get_all_assemblies():
    """Fetch all assemblies from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM assemblies")
    assemblies = c.fetchall()
    conn.close()
    return assemblies

def get_assembly_details(assembly_name):
    """Fetch tray assignments for a specific assembly from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, tray_1, tray_2, tray_3 FROM assemblies WHERE name = ?", (assembly_name,))
    assembly_details = c.fetchone()
    conn.close()
    return assembly_details

