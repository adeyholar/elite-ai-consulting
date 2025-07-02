from datetime import datetime, timedelta
from services.ollama_client import OllamaClient

class TaskAgent:
    def __init__(self):
        self.ollama_client = OllamaClient()

    def process_task(self, task_id, desc, time_str, priority, recurring):
        """
        Process a task, schedule it, and generate an AI response.
        """
        try:
            # Schedule task
            if time_str:
                today = datetime.now().date()
                scheduled_time = datetime.strptime(time_str, "%H:%M").time()
                scheduled_dt = datetime.combine(today, scheduled_time)
                if scheduled_dt < datetime.now():
                    scheduled_dt += timedelta(days=1)
                schedule_info = f"Scheduled for {scheduled_dt.strftime('%Y-%m-%d %H:%M')}"
            else:
                schedule_info = "No specific time set"

            # Generate AI confirmation
            prompt = f"Confirm that the task '{desc}' has been scheduled with priority {priority} and {'recurring' if recurring else 'one-time'} status. {schedule_info}"
            response = self.ollama_client.generate(prompt, model="llama3.2:latest")
            
            return {
                'description': desc,
                'time': time_str,
                'priority': priority,
                'recurring': recurring,
                'status': 'Scheduled',
                'ai_response': response
            }
        except ValueError as e:
            return {
                'description': desc,
                'time': time_str,
                'priority': priority,
                'recurring': recurring,
                'status': 'Error',
                'ai_response': f"Error processing task: Invalid time format ({e})"
            }