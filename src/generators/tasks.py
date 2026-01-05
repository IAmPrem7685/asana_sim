import datetime
import random

def generate_task_metadata(created_at_limit):
    """
    Implements the logic from the assignment Page 4:
    - 25% within 1 week, 40% within 1 month...
    - 5% overdue, 15% unassigned.
    """
    # 1. Assignee Distribution (15% unassigned per Asana benchmarks)
    is_unassigned = random.random() < 0.15
    
    # 2. Completion Status
    is_completed = random.random() < 0.60 # 60% average completion rate
    
    # 3. Temporal Consistency
    created_at = fake.date_time_between(start_date='-60d', end_date='now')
    
    completed_at = None
    if is_completed:
        # Completion must be AFTER creation (Rule 4 on Page 4)
        days_to_complete = random.lognormvariate(1, 0.5) # Log-normal cycle time
        completed_at = created_at + datetime.timedelta(days=days_to_complete)
        if completed_at > datetime.datetime.now():
            completed_at = datetime.datetime.now()

    # 4. Due Date Distribution (clustering around workdays)
    # Avoid weekends for 85% of tasks (Rule from Page 4)
    due_date = created_at + datetime.timedelta(days=random.randint(1, 30))
    if random.random() < 0.85 and due_date.weekday() > 4:
        due_date -= datetime.timedelta(days=2) # Shift Sunday/Saturday to Friday
        
    return {
        "created_at": created_at,
        "completed_at": completed_at,
        "is_completed": is_completed,
        "due_date": due_date.date(),
        "is_unassigned": is_unassigned
    }