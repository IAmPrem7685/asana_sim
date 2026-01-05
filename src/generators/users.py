import uuid
from faker import Faker
import random

fake = Faker()

def generate_users_and_teams(num_users):
    users = []
    teams = [
        {"name": "Engineering", "ratio": 0.40},
        {"name": "Product", "ratio": 0.10},
        {"name": "Marketing", "ratio": 0.15},
        {"name": "Sales", "ratio": 0.20},
        {"name": "Customer Success", "ratio": 0.15}
    ]
    
    # 1. Create Organization
    org_id = str(uuid.uuid4())
    org = {"org_id": org_id, "name": "CloudScale AI", "domain": "cloudscale.ai"}

    # 2. Create Teams
    for t in teams:
        t["id"] = str(uuid.uuid4())

    # 3. Create Users with Role Distribution
    for _ in range(num_users):
        # Pick a team based on defined SaaS ratios
        assigned_team = random.choices(teams, weights=[t["ratio"] for t in teams])[0]
        
        user_role = random.choices(['member', 'admin', 'guest'], weights=[0.85, 0.05, 0.10])[0]
        
        users.append({
            "user_id": str(uuid.uuid4()),
            "org_id": org_id,
            "full_name": fake.name(),
            "email": fake.email(),
            "role": user_role,
            "team_id": assigned_team["id"] # We'll use this for membership table
        })
        
    return org, teams, users