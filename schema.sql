-- Organizations Table
CREATE TABLE organizations (
    org_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users Table
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT CHECK(role IN ('admin', 'member', 'guest')),
    created_at TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- Teams Table
CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- Projects Table
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    owner_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('on_track', 'at_risk', 'off_track')),
    created_at TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

-- Sections Table
CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    rank INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Tasks Table (Self-referencing for Subtasks)
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    section_id TEXT NOT NULL,
    assignee_id TEXT,
    creator_id TEXT NOT NULL,
    parent_task_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    created_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    is_completed BOOLEAN DEFAULT 0,
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id),
    FOREIGN KEY (creator_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id)
);

-- Custom Fields Definitions
CREATE TABLE custom_field_definitions (
    field_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    field_type TEXT CHECK(field_type IN ('text', 'number', 'enum')),
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- Custom Field Values (EAV Model)
CREATE TABLE custom_field_values (
    value_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    field_id TEXT NOT NULL,
    value TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id)
);