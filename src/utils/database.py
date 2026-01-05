import sqlite3
import os

def init_db(db_path, schema_path):
    """Initializes the SQLite database using the DDL schema."""
    if os.path.exists(db_path):
        os.remove(db_path) # Start fresh for the simulation
    
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    return conn