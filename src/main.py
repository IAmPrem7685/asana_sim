import os
import sqlite3
import random
from datetime import datetime, timedelta
from utils.database import init_db
from utils.llm_client import AsanaDataLLM
from generators.users import generate_users_and_teams
from generators.projects import generate_projects_and_sections

def main():
    db_path = "output/asana_simulation.sqlite"
    if os.path.exists(db_path): 
        os.remove(db_path)
        print("🗑️ Existing database removed.")
    
    conn = init_db(db_path, "schema.sql")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    llm = AsanaDataLLM()
    depts = ["Engineering", "Product", "Marketing", "Sales", "Customer Success"]
    
    # 1. Generate Core Data
    print("🧬 Generating Users and Teams...")
    org, teams, users = generate_users_and_teams(500)
    
    print("🏗️ Generating Projects and Sections...")
    projects, sections = generate_projects_and_sections(teams, users)
    
    # Map project to team name for the LLM pool selection
    team_name_map = {t['team_id']: t['name'] for t in teams}
    for p in projects:
        p['team_name'] = team_name_map.get(p['team_id'], "Engineering")

    print("🤖 Bulk fetching task names from Gemini...")
    task_pools = llm.generate_all_department_tasks(depts)

    # 2. Setup Custom Fields
    field_defs = [
        (str(random.getrandbits(64)), org['org_id'], 'Priority', 'enum'),
        (str(random.getrandbits(64)), org['org_id'], 'Story Points', 'number'),
        (str(random.getrandbits(64)), org['org_id'], 'Environment', 'text')
    ]

    # 3. Task Generation Loop
    tasks_to_insert = []
    cf_values_to_insert = []
    now_str = datetime.now().isoformat()

    print("📝 Preparing Task batches...")
    for section in sections:
        # Get the department name from the project associated with this section
        project_id = section['project_id']
        dept = next((p['team_name'] for p in projects if p['project_id'] == project_id), "Engineering")
        
        # Get task list from LLM pool
        pool = task_pools.get(dept)
        if not pool: pool = [f"[{dept}] Follow-up Task {i}" for i in range(10)]
        
        for _ in range(random.randint(5, 10)):
            t_id = str(random.getrandbits(128))
            created_at = (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat()
            
            # Match schema: task_id, section_id, assignee_id, creator_id, parent_task_id, 
            # name, description, due_date, created_at, completed_at, is_completed
            tasks_to_insert.append((
                t_id, 
                section['section_id'], 
                random.choice(users)['user_id'],
                users[0]['user_id'], 
                None, 
                random.choice(pool), 
                "Simulated task description", 
                (datetime.now() + timedelta(days=7)).date().isoformat(), 
                created_at, 
                None, 
                0
            ))

            # Assign Priority Custom Field Value
            cf_values_to_insert.append((
                str(random.getrandbits(128)), 
                t_id, 
                field_defs[0][0], 
                random.choice(['Low', 'Medium', 'High', 'Urgent'])
            ))

    # 4. Database Insertion
    try:
        cursor.execute("INSERT INTO organizations VALUES (?, ?, ?, ?)", 
                       (org['org_id'], org['name'], org['domain'], now_str))
        
        cursor.executemany("INSERT INTO users (user_id, org_id, full_name, email, role, created_at) VALUES (?,?,?,?,?,?)", 
                           [(u['user_id'], u['org_id'], u['full_name'], u['email'], u['role'], now_str) for u in users])
        
        cursor.executemany("INSERT INTO teams VALUES (?, ?, ?)", 
                           [(t['team_id'], t['org_id'], t['name']) for t in teams])
        
        cursor.executemany("INSERT INTO projects VALUES (?,?,?,?,?,?,?)",
                           [(p['project_id'], p['team_id'], p['owner_id'], p['name'], p['description'], p['status'], now_str) for p in projects] )
        
        cursor.executemany("INSERT INTO sections VALUES (?,?,?,?)", 
                           [(s['section_id'], s['project_id'], s['name'], s['rank']) for s in sections])
        
        # Bulk Insert Tasks
        cursor.executemany("INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?,?,?)", tasks_to_insert)

        # Bulk Insert Custom Fields
        cursor.executemany("INSERT INTO custom_field_definitions VALUES (?,?,?,?)", field_defs)
        cursor.executemany("INSERT INTO custom_field_values VALUES (?,?,?,?)", cf_values_to_insert)
        
        conn.commit()
        
        # Final Verification Print
        cursor.execute("SELECT COUNT(*) FROM tasks")
        final_count = cursor.fetchone()[0]
        print(f"✅ Success! Database populated.")
        print(f"📊 Summary: {len(users)} Users | {len(projects)} Projects | {final_count} Tasks.")

    except sqlite3.Error as e:
        print(f"❌ DB Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()