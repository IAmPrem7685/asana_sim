import uuid
import random
from datetime import datetime, timedelta

class TaskGenerator:
    def __init__(self, llm_client, departments):
        print("🚀 Bulk fetching task names for all departments...")
        # One call to rule them all
        self.pools = llm_client.generate_all_department_tasks(departments)

    def get_task_name(self, dept):
        # Fallback if a department wasn't in the initial call
        if dept not in self.pools or not self.pools[dept]:
            return f"General {dept} Task"
        
        # Pop a name to keep tasks unique within the run
        return self.pools[dept].pop(random.randrange(len(self.pools[dept])))