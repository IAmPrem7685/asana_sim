import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

class AsanaDataLLM:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        self.model_id = "gemini-2.0-flash"
        
        # Load the local JSON fallback data
        self.fallback_path = os.path.join(os.path.dirname(__file__), "tasks_fallback.json")
        with open(self.fallback_path, 'r') as f:
            self.local_tasks = json.load(f)

    def generate_all_department_tasks(self, departments):
        """Attempts Gemini call, falls back to local JSON on failure."""
        if self.client:
            try:
                print("✨ Attempting bulk task generation via Gemini...")
                prompt = f"Generate 20 SaaS task names for these depts: {', '.join(departments)}. Return JSON object."
                
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt,
                    config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text)
            except Exception as e:
                print(f"⚠️ Gemini API failed: {e}. Switching to local fallback.")
        
        # Return local data if API is missing or fails
        # We use .get() to return a generic list if the department isn't in our JSON
        return {dept: self.local_tasks.get(dept, [f"[{dept}] Generic Task"]) for dept in departments}