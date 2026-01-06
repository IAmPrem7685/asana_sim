import uuid
import random

def generate_projects_and_sections(teams, users):
    projects = []
    sections = []
    
    # Project naming templates for different departments
    project_templates = {
        "Engineering": ["Core Platform", "Mobile App", "API Infrastructure", "Security Audit"],
        "Product": ["Roadmap 2026", "User Research", "Feature Specs"],
        "Marketing": ["Q1 Campaign", "Brand Refresh", "Social Media Content"],
        "Sales": ["Enterprise Pipeline", "Partner Program"],
        "Customer Success": ["Onboarding Flow", "Knowledge Base Expansion"]
    }

    # Standard Kanban sections
    section_names = ["Backlog", "In Progress", "Review", "Done"]

    for team in teams:
        # Determine how many projects this team has (1-3)
        team_name = team['name']
        num_projects = random.randint(1, 3)
        
        # Get users belonging to this specific team to pick an owner
        team_users = [u for u in users if u.get('team_id') == team['team_id']]
        
        # Fallback to any user if team is empty (safeguard)
        potential_owners = team_users if team_users else users

        templates = project_templates.get(team_name, ["General Initiatives"])
        
        for i in range(num_projects):
            project_id = str(uuid.uuid4())
            owner = random.choice(potential_owners)
            
            project = {
                "project_id": project_id,
                "team_id": team['team_id'],
                "owner_id": owner['user_id'],
                "name": random.choice(templates) + f" ({i+1})",
                "description": f"Main project for {team_name} operations.",
                "status": random.choice(['on_track', 'at_risk', 'off_track'])
            }
            projects.append(project)

            # Create 4 sections for every project
            for rank, s_name in enumerate(section_names):
                sections.append({
                    "section_id": str(uuid.uuid4()),
                    "project_id": project_id,
                    "name": s_name,
                    "rank": rank
                })

    return projects, sections