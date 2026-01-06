SYSTEM_PROMPT = """You are an expert Project Manager at a top-tier B2B SaaS company. 
Your goal is to generate highly realistic Asana data. 
Avoid generic terms like 'Task 1'. Use industry-specific terminology 
(e.g., 'Kubernetes pods', 'GTM strategy', 'Churn rate', 'API rate limiting')."""

TASK_NAME_PROMPT = """Generate a JSON list of 20 unique task names for the {department} department.
Patterns to follow:
- Engineering: [Component] - [Action] - [Detail] (e.g., [Auth] - Fix - OAuth callback timeout)
- Marketing: [Campaign] - [Deliverable] (e.g., [Q1 Launch] - Draft - Press release)
- Product: [Feature] - [Stage] (e.g., [Search] - Research - User interview summaries)

Return ONLY a JSON object: {{"tasks": ["name1", "name2", ...]}}"""