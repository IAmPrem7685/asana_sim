from utils.database import init_db
from generators.users import generate_users_and_teams
import os

def main():
    # 1. Setup
    db_path = "output/asana_simulation.sqlite"
    
    # 1. Reset Database: Delete the existing file to avoid Unique Constraint errors
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Existing database at {db_path} removed for a fresh run.")

    conn = init_db(db_path, "schema.sql")
    cursor = conn.cursor()

    # 2. Generate Entities
    org, teams, users = generate_users_and_teams(5000)

    # 3. Bulk Insert (Example for Users)
    user_data = [(u['user_id'], u['org_id'], u['full_name'], u['email'], u['role']) for u in users]
    cursor.executemany(
    "INSERT OR IGNORE INTO users (user_id, org_id, full_name, email, role) VALUES (?, ?, ?, ?, ?)", 
    user_data
)
    
    # Repeat for teams, projects, and tasks...
    
    conn.commit()
    conn.close()
    print(f"Success! Database generated at {db_path}")

if __name__ == "__main__":
    main()